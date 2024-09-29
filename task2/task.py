import pandas as pd
import sys

def find_root(edges):
    not_leaf_vertices = set(edges.keys())

    for v in edges.keys():
        for to in edges[v]:
            not_leaf_vertices.discard(to)
        
    return list(not_leaf_vertices)[0]

def find_nearest_childs_cnt(v, edges):
    if v in edges.keys():
        return len(edges[v])
    return 0

def find_all_childs_cnt(v, edges):
    # если лист, то 0 детей
    if v not in edges.keys():
        return 0
    
    total_childs = len(edges[v])
    for to in edges[v]:
        total_childs += find_all_childs_cnt(to, edges)

    return total_childs
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python task.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    df = pd.read_csv(file_path, header=None)
    edges = dict()
    
    # Структура дерева
    for edge_num, edge in df.iterrows():
        from_vertice = int(edge[0])
        to_vertice = int(edge[1])
        edges.setdefault(from_vertice, [])
        edges[from_vertice].append(to_vertice)