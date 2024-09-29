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

def find_depth(v, edges, depth_dict, d=0):
    depth_dict[v] = d
    # если вершина - лист, то никуда дальше не идем
    if v not in edges.keys():
        return 0
    # ищем глубины дальше
    for to in edges[v]:
        find_depth(to, edges, depth_dict, d+1)
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python task.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    df = pd.read_csv(file_path, header=None)
    edges = dict()
    
    vertices = []
    # Структура дерева
    for edge_num, edge in df.iterrows():
        from_vertice = int(edge[0])
        to_vertice = int(edge[1])
        vertices.extend([from_vertice, to_vertice])
        edges.setdefault(from_vertice, [])
        edges[from_vertice].append(to_vertice)
    vertices = list(set(vertices))
    vertices = sorted(vertices)

    final_answer = pd.DataFrame(columns=['r1', 'r2', 'r3', 'r4', 'r5'])

    for v in vertices:
        ans = dict.fromkeys(['r1', 'r2', 'r3', 'r4', 'r5'])
        # r1 - непосредственное управление
        ans['r1'] = find_nearest_childs_cnt(v, edges)
        # r2 - отношение непосредственного подчинения
        root = find_root(edges)
        ans['r2'] = int(root != v)
        # r3 - отношение опосредственного управления
        ans['r3'] = find_all_childs_cnt(v, edges) - ans['r1']
        # r4 - отношение опосредованного подчинения
        depth_dict = dict.fromkeys(vertices, 0)
        find_depth(root, edges, depth_dict)
        ans['r4'] = max(0, depth_dict[v] - 1)
        # r5 - отношение соподчинения на одном уровне
        ans['r5'] = max(0, len([x for x in depth_dict.keys() if depth_dict[x] == depth_dict[v]]) - 1)

        ans = pd.DataFrame([ans], index=[v])

        final_answer = pd.concat([final_answer, ans], ignore_index=False)

    final_answer.to_csv("result.csv", header=None, index=None)