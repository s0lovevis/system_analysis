import json
import numpy as np

def create_relationship_matrix(ordering, size):
    relation_matrix = np.zeros((size, size), dtype=int)
    ordering = [group if isinstance(group, list) else [group] for group in ordering]
    
    for i, group in enumerate(ordering):
        for element in group:
            for j in range(i, len(ordering)):
                for related_element in ordering[j]:
                    relation_matrix[element - 1][related_element - 1] = 1
    return relation_matrix

def detect_conflict_core(matrix_A, matrix_B, size):
    conflict_pairs = []
    
    A_dom = (matrix_A == 1) & (matrix_A.T == 0)
    B_dom = (matrix_B == 0) & (matrix_B.T == 1)
    
    for row in range(size):
        for col in range(size):
            if row != col and A_dom[row, col] and B_dom[row, col]:
                conflict_pairs.append((row + 1, col + 1))
                
    return conflict_pairs

def main(json_str1, json_str2):

    rankings_A = [group if isinstance(group, list) else [group] for group in json.loads(json_str1)]
    rankings_B = [group if isinstance(group, list) else [group] for group in json.loads(json_str2)]

    matrix_size = max(item for group in rankings_A + rankings_B for item in group)

    matrix_A = create_relationship_matrix(rankings_A, matrix_size)
    matrix_B = create_relationship_matrix(rankings_B, matrix_size)

    conflict_core = detect_conflict_core(matrix_A, matrix_B, matrix_size)

    return json.dumps(conflict_core)


# Тест
json_str1 = '[1, [2, 3], 4, [5, 6, 7], 8, 9, 10]'
json_str2 = '[[1, 2], [3, 4, 5], 6, 7, 9, [8, 10]]'
result = main(json_str1, json_str2)
print(result)