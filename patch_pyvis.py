import re
with open("network.html", "r") as f:
    data = f.read()

data = data.replace('allNodes[nodeId].color = "rgba(200,200,200,0.5)";', 
                    'allNodes[nodeId].color = "rgba(200,200,200,0.5)";\n      allNodes[nodeId].hidden = true;')
data = data.replace('allNodes[allConnectedNodes[i]].color = "rgba(150,150,150,0.75)";',
                    'allNodes[allConnectedNodes[i]].color = "rgba(150,150,150,0.75)";\n      allNodes[allConnectedNodes[i]].hidden = false;')
data = data.replace('allNodes[connectedNodes[i]].color = nodeColors[connectedNodes[i]];',
                    'allNodes[connectedNodes[i]].color = nodeColors[connectedNodes[i]];\n      allNodes[connectedNodes[i]].hidden = false;')
data = data.replace('allNodes[selectedNode].color = nodeColors[selectedNode];',
                    'allNodes[selectedNode].color = nodeColors[selectedNode];\n    allNodes[selectedNode].hidden = false;')
data = data.replace('allNodes[nodeId].color = nodeColors[nodeId];',
                    'allNodes[nodeId].color = nodeColors[nodeId];\n      allNodes[nodeId].hidden = false;')

with open("network_patched.html", "w") as f:
    f.write(data)
