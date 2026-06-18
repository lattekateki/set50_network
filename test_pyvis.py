from pyvis.network import Network
net = Network(filter_menu=True, select_menu=True)
net.add_node(1, label="Node 1")
net.add_node(2, label="Node 2")
net.add_edge(1, 2)
net.save_graph("test_net.html")
