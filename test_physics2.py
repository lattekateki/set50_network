from pyvis.network import Network
import json

net = Network()
net.force_atlas_2based()
net.set_options('{"physics": {"stabilization": false}}')
print(net.options.to_json())
