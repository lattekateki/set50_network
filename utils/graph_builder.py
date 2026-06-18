"""
graph_builder.py — Build NetworkX graph from SET50 stakeholder data.
Compute centrality metrics and provide filtering utilities.
"""
import networkx as nx
import pandas as pd
from typing import Optional, List, Dict
from utils.data_fetcher import _get_sector_color, STAKEHOLDER_COLORS


def build_graph(
    stock_info: dict,
    edges: list,
    selected_sectors: Optional[list] = None,
) -> nx.Graph:
    """
    Build a NetworkX graph from fetched data.

    Nodes:
      - Company nodes: symbol, name, industry, sector, node_type="Company"
      - Stakeholder nodes: name, node_type="Shareholder" or "Director"

    Edges:
      - Company ↔ Stakeholder (with optional weight = percent_share)
    """
    G = nx.Graph()

    # Filter companies by sector if specified
    active_symbols = set()
    for sym, info in stock_info.items():
        industry = info.get("industry", "")
        if selected_sectors and industry not in selected_sectors:
            continue
        active_symbols.add(sym)
        G.add_node(
            sym,
            label=sym,
            title=f"Company: {sym}\nName: {info.get('name_en', sym)}\nSector: {info.get('sector', '')}",
            name=info.get("name_en", sym),
            name_th=info.get("name_th", ""),
            industry=industry,
            sector=info.get("sector", ""),
            node_type="Company",
            color=_get_sector_color(industry),
            size=20,
        )

    # Add stakeholder nodes and edges
    for edge in edges:
        company = edge["company"]
        if company not in active_symbols:
            continue

        stakeholder_name = edge["stakeholder_name"]
        stakeholder_type = edge["stakeholder_type"]

        # Add stakeholder node (if not exists)
        if not G.has_node(stakeholder_name):
            G.add_node(
                stakeholder_name,
                label=stakeholder_name[:20] + "..." if len(stakeholder_name) > 20 else stakeholder_name,
                title=f"{stakeholder_type}: {stakeholder_name}",
                name=stakeholder_name,
                node_type=stakeholder_type,
                color=STAKEHOLDER_COLORS.get(stakeholder_type, "#94A3B8"),
                size=15,
            )

        # Add edge
        edge_attrs = {"relationship": stakeholder_type}
        title_str = f"{stakeholder_type}"
        if edge.get("percent_share") is not None:
            edge_attrs["weight"] = edge["percent_share"]
            title_str += f"\nShare: {edge['percent_share']}%"
        if edge.get("positions"):
            edge_attrs["positions"] = edge["positions"]
            title_str += f"\nPositions: {edge['positions']}"
        edge_attrs["title"] = title_str

        G.add_edge(company, stakeholder_name, **edge_attrs)

    return G


def compute_metrics(G: nx.Graph) -> dict:
    """Compute summary metrics for the graph."""
    if G.number_of_nodes() == 0:
        return {
            "total_nodes": 0,
            "total_edges": 0,
            "density": 0.0,
            "most_connected_node": "N/A",
            "most_connected_type": "",
            "most_connected_degree": 0,
        }

    degrees = dict(G.degree())
    most_connected = max(degrees, key=degrees.get)
    node_data = G.nodes[most_connected]

    return {
        "total_nodes": G.number_of_nodes(),
        "total_edges": G.number_of_edges(),
        "density": nx.density(G),
        "most_connected_node": most_connected,
        "most_connected_type": node_data.get("node_type", ""),
        "most_connected_degree": degrees[most_connected],
    }


def get_top_connected(G: nx.Graph, n: int = 10) -> pd.DataFrame:
    """
    Get top-N most connected nodes as a DataFrame.
    Columns: Node, Type, Connections, Centrality
    """
    if G.number_of_nodes() == 0:
        return pd.DataFrame(columns=["Node", "Type", "Connections", "Centrality"])

    centrality = nx.degree_centrality(G)
    degrees = dict(G.degree())

    rows = []
    for node in G.nodes():
        node_data = G.nodes[node]
        rows.append({
            "Node": node,
            "Type": node_data.get("node_type", "Unknown"),
            "Connections": degrees.get(node, 0),
            "Centrality": round(centrality.get(node, 0), 4),
        })

    df = pd.DataFrame(rows)
    df = df.sort_values("Connections", ascending=False).head(n).reset_index(drop=True)
    return df


def get_subgraph_for_node(G: nx.Graph, node: str) -> nx.Graph:
    """Extract subgraph: the selected node + all its direct neighbors."""
    if node not in G:
        return nx.Graph()
    neighbors = list(G.neighbors(node))
    sub_nodes = [node] + neighbors
    return G.subgraph(sub_nodes).copy()


def get_company_nodes(G: nx.Graph) -> list[str]:
    """Return sorted list of company nodes in the graph."""
    companies = [
        n for n, d in G.nodes(data=True)
        if d.get("node_type") == "Company"
    ]
    return sorted(companies)
