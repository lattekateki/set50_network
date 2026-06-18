import networkx as nx
from utils.data_fetcher import fetch_network_data, SET50_SYMBOLS
from utils.graph_builder import build_graph

stock_info, edges = fetch_network_data(tuple(SET50_SYMBOLS), mode="shareholders", lang="th")
G = build_graph(stock_info, edges)

edge_data = G.get_edge_data("AOT", "กระทรวงการคลัง")
print("Edge data for AOT - กระทรวงการคลัง:", edge_data)
