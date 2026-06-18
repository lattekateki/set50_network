import re
import json
from collections import defaultdict

with open("network.html", "r", encoding="utf-8") as f:
    content = f.read()

# Extract the dataset array
edges_match = re.search(r'edges = new vis\.DataSet\(\[(.*?)\]\);', content, re.DOTALL)
if edges_match:
    edges_str = "[" + edges_match.group(1) + "]"
    edges = json.loads(edges_str)
    
    director_companies = defaultdict(list)
    for e in edges:
        if e.get("relationship") == "Director":
            comp = e.get("from")
            person = e.get("to")
            if comp and person:
                # normalize name to avoid case sensitivity issues
                person_norm = person.strip().upper()
                if comp not in director_companies[person_norm]:
                    director_companies[person_norm].append(comp)
    
    multiple = {k: v for k, v in director_companies.items() if len(v) >= 2}
    
    print(f"Found {len(multiple)} directors sitting on multiple boards:")
    for p, comps in sorted(multiple.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"- {p} sits on {len(comps)} boards: {', '.join(comps)}")
else:
    print("Could not parse edges.")

