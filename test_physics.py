from pyvis.network import Network

net = Network(height="600px", width="100%", bgcolor="#0E1117", font_color="#E2E8F0", select_menu=True, cdn_resources="in_line")
net.add_node(1)
net.add_node(2)
net.add_edge(1, 2)
net.force_atlas_2based()
net.set_options('{"physics": {"stabilization": false}}')
net.save_graph("test_physics.html")
