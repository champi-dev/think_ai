import sys

#!/usr / bin / env python3


try:
from pymilvus import Collection, connections, utility

    connections.connect("default", host="localhost", port="19530")
    for c in utility.list_collections():
        Collection(c).drop()
        connections.disconnect("default")
        except Exception:
            pass
        sys.exit(0)
