import pandas as pd
from collections import defaultdict
from pprint import pprint
from collections import defaultdict
from pprint import pprint

def build_adjacency_list(edges, verbose=False):
    network = defaultdict(set)
    nodes = set()
    try:
        for _, row in edges.iterrows():
            if len(row) < 2:
                if verbose:
                    print(f"⚠️  Warning: Skipping malformed row with {len(row)} columns")
                continue 

            node1, node2 = row[0], row[1]

            if isinstance(node1, (int, float)) and not isinstance(node1, bool):
                node1 = int(node1)
            if isinstance(node2, (int, float)) and not isinstance(node2, bool):
                node2 = int(node2)

            network[node1].add(node2)
            network[node2].add(node1)
            nodes.add(node1)
            nodes.add(node2)

        if verbose:
            print("\nFinal Adjacency List:")
            pprint(dict(network))

        return network, list(nodes)

    except Exception as e:
        if verbose:
            print(f" Error while building adjacency list: {e}")
        raise

def load_network(file_path, verbose=False):
    try:
        edges = pd.read_csv(file_path, sep='\t', header=None, skiprows=1)
        
        if edges.empty:
            if verbose:
                print("Warning: Empty network detected.")
            return {}, [] 
        
        return build_adjacency_list(edges, verbose)
    
    except pd.errors.EmptyDataError:
        if verbose:
            print("Warning: Empty or malformed file detected.")
        return {}, []
    
    except Exception as e:
        if verbose:
            print(f"Error loading network: {e}")
        raise