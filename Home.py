"""
Home.py — Main Streamlit application file for SET50 Stakeholder Network
"""
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
from pyvis.network import Network

from utils.styles import inject_global_styles, render_kpi_card, render_legend, render_top_table
from utils.data_fetcher import fetch_network_data, get_available_sectors, SET50_SYMBOLS, SECTOR_COLORS, STAKEHOLDER_COLORS
from utils.graph_builder import build_graph, compute_metrics, get_top_connected, get_subgraph_for_node, get_company_nodes

st.set_page_config(
    page_title="SET50 Stakeholder Network",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_styles()

# ---------------------------------------------------------------------------
# Sidebar Configuration
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🌐 SET50 Stakeholder Network")
    st.markdown(
        "Visualize relationships between Thailand's top 50 listed companies and their key stakeholders.",
        help="Data provided by settfex"
    )
    st.markdown("---")
    
    st.markdown("### ⚙️ Configuration")
    
    lang_choice = st.radio("Language / ภาษา", ["EN English", "TH ภาษาไทย"], index=0)
    lang_code = "en" if "EN" in lang_choice else "th"
    
    mode_choice = st.selectbox(
        "Stakeholder Mode",
        ["Major Shareholders (Top 5)", "Board of Directors", "Both (Shareholders & Directors)"],
        index=0
    )
    
    if "Shareholders" in mode_choice and "Directors" in mode_choice:
        mode = "both"
    elif "Directors" in mode_choice:
        mode = "directors"
    else:
        mode = "shareholders"
        
# Fetch data early to populate dynamic filters
stock_info, edges = fetch_network_data(tuple(SET50_SYMBOLS), mode=mode, lang=lang_code)
available_sectors = get_available_sectors(stock_info)

with st.sidebar:
    st.markdown("---")
    st.markdown("### Filter by Sector")
    
    selected_sectors = st.multiselect(
        "Select Sectors to Include",
        options=available_sectors,
        default=available_sectors,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown(
        f"<div class='footer-text'>Data Source: SET via settfex<br>Last refresh: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>",
        unsafe_allow_html=True
    )

# ---------------------------------------------------------------------------
# Process Graph Data
# ---------------------------------------------------------------------------
G = build_graph(stock_info, edges, selected_sectors=selected_sectors)
metrics = compute_metrics(G)
top_nodes_df = get_top_connected(G, n=10)

# ---------------------------------------------------------------------------
# Main UI Layout
# ---------------------------------------------------------------------------
title = "SET50 Major Shareholders and Board of Directors" if mode == "both" else ("SET50 Major Shareholders" if mode == "shareholders" else "SET50 Board of Directors")

st.markdown(
    f"""
    <div class="banner-container">
        <div class="banner-title">{title}</div>
        <div class="banner-subtitle">Interactive network analysis of corporate relationships in the Stock Exchange of Thailand</div>
    </div>
    """,
    unsafe_allow_html=True
)

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    render_kpi_card("TOTAL NODES", f"{metrics['total_nodes']:,}", color="#3B82F6")
with col2:
    render_kpi_card("TOTAL CONNECTIONS", f"{metrics['total_edges']:,}", color="#10B981")
with col3:
    val = str(metrics['most_connected_node'])
    fs = "1.2rem" if len(val) > 15 else "1.8rem"
    render_kpi_card("MOST CONNECTED", val, color="#8B5CF6", font_size=fs)
with col4:
    render_kpi_card("NETWORK DENSITY", f"{metrics['density']:.4f}", color="#F59E0B")

st.markdown("<br>", unsafe_allow_html=True)

# Top Connected Nodes Table
st.markdown("### 🔗 Top 10 Most Connected Nodes")
render_top_table(top_nodes_df)

st.markdown("<br>", unsafe_allow_html=True)

# Legend
st.markdown("### 🎨 Legend")
render_legend(selected_sectors)

st.markdown("<br>", unsafe_allow_html=True)

# Interactive Network
st.markdown("### 🕸️ Interactive Network")
st.markdown("<span style='color:#94A3B8;font-size:0.85rem;'>Drag nodes to interact · Scroll to zoom · Hover for details</span>", unsafe_allow_html=True)

if G.number_of_nodes() > 0:
    net = Network(height="600px", width="100%", bgcolor="#0E1117", font_color="#E2E8F0", select_menu=True, cdn_resources="in_line")
    net.force_atlas_2based()
    net.toggle_stabilization(False)
    net.from_nx(G)
    
    net_html = "network.html"
    net.save_graph(net_html)
    
    with open(net_html, 'r', encoding='utf-8') as f:
        html_data = f.read()

    # Hide the PyVis loading bar since we disabled stabilization
    html_data = html_data.replace(
        '</head>',
        '<style>#loadingBar { display: none !important; }</style>\n</head>'
    )

    # --- INJECT JS TO HIDE UNRELATED NODES ---
    html_data = html_data.replace(
        'allNodes[nodeId].color = "rgba(200,200,200,0.5)";',
        'allNodes[nodeId].color = "rgba(200,200,200,0.5)";\n      allNodes[nodeId].hidden = true;'
    )
    html_data = html_data.replace(
        'allNodes[allConnectedNodes[i]].color = "rgba(150,150,150,0.75)";',
        'allNodes[allConnectedNodes[i]].color = nodeColors[allConnectedNodes[i]];\n      allNodes[allConnectedNodes[i]].hidden = false;'
    )
    html_data = html_data.replace(
        'allNodes[connectedNodes[i]].color = nodeColors[connectedNodes[i]];',
        'allNodes[connectedNodes[i]].color = nodeColors[connectedNodes[i]];\n      allNodes[connectedNodes[i]].hidden = false;'
    )
    html_data = html_data.replace(
        'allNodes[selectedNode].color = nodeColors[selectedNode];',
        'allNodes[selectedNode].color = nodeColors[selectedNode];\n    allNodes[selectedNode].hidden = false;'
    )
    html_data = html_data.replace(
        'allNodes[nodeId].color = nodeColors[nodeId];',
        'allNodes[nodeId].color = nodeColors[nodeId];\n      allNodes[nodeId].hidden = false;'
    )
    # -----------------------------------------

    components.html(html_data, height=620)
else:
    st.info("No data available for the selected filters.")

st.markdown("<br>", unsafe_allow_html=True)

# Node Profiler
st.markdown("### 🔍 Node Profiler")

with st.container(border=True):
    all_nodes = sorted(list(G.nodes()))
    selected_node = st.selectbox("Search / Select Node", options=["-- Select a Node --"] + all_nodes)
    
    st.markdown("---")
    
    if selected_node and selected_node != "-- Select a Node --":
        node_data = G.nodes[selected_node]
        sub_g = get_subgraph_for_node(G, selected_node)
        
        st.markdown(f"**Name:** {node_data.get('name', selected_node)}")
        st.markdown(f"**Type:** {node_data.get('node_type', 'Unknown')}")
        if node_data.get("industry"):
            st.markdown(f"**Industry:** {node_data.get('industry')}")
            
        st.markdown(f"**Connections:** {sub_g.number_of_nodes() - 1}")
        
        st.markdown("#### Direct Connections")
        connections = []
        for n in sub_g.nodes():
            if n != selected_node:
                edge_data = G.get_edge_data(selected_node, n) or {}
                rel = edge_data.get('relationship', '')
                weight = edge_data.get('weight', edge_data.get('width', ''))
                
                try:
                    w_val = float(weight) if weight not in ('', None) else 0.0
                except ValueError:
                    w_val = 0.0
                    
                connections.append({
                    "name": n,
                    "rel": rel,
                    "weight_val": w_val,
                    "weight_orig": weight
                })
                
        # Sort descending by default (most shares first)
        connections.sort(key=lambda x: x["weight_val"], reverse=True)
        
        for conn in connections:
            w_orig = conn["weight_orig"]
            weight_str = f" ({w_orig}%)" if w_orig not in ('', None) else ""
            st.markdown(f"- {conn['name']} <span style='color:#64748B;font-size:0.8rem;'>{conn['rel']}{weight_str}</span>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='profiler-info'>Select a node from the dropdown above to profile its direct connections and attributes.</div>", unsafe_allow_html=True)
