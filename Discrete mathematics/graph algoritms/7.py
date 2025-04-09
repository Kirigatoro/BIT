import pandas as pd
from itertools import combinations
import string

def magu_weisman_algorithm(edges, num_vertices):
    vertex_labels = list(string.ascii_lowercase)[:num_vertices]
    label_to_idx = {label: idx + 1 for idx, label in enumerate(vertex_labels)}
    edges_numeric = [(label_to_idx[u], label_to_idx[v]) for u, v in edges]
    
    # Step 1: Build formula Πg
    sorted_edges = sorted(edges, key=lambda x: (x[0], x[1]))
    formula_pg = "*".join([f"({u}+{v})" for u, v in sorted_edges])
    
    # Step 2-3: Find all maximal independent sets (MIS)
    def is_independent_set(vertex_set, edges_numeric):
        vertex_set_numeric = set(label_to_idx[v] for v in vertex_set)
        for u in vertex_set_numeric:
            for v in vertex_set_numeric:
                if u != v and ((u, v) in edges_numeric or (v, u) in edges_numeric):
                    return False
        return True

    all_vertices = set(vertex_labels)
    maximal_independent_sets = []
    for r in range(num_vertices, 0, -1):
        for comb in combinations(vertex_labels, r):
            comb_set = set(comb)
            if is_independent_set(comb_set, edges_numeric):
                is_maximal = True
                for v in all_vertices - comb_set:
                    if is_independent_set(comb_set | {v}, edges_numeric):
                        is_maximal = False
                        break
                if is_maximal:
                    maximal_independent_sets.append(sorted(list(comb_set)))
    
    # Complements for Πg DNF (optional for verification)
    complements = [sorted(list(all_vertices - set(mis))) for mis in maximal_independent_sets]
    dnf_terms = ["*".join(comp) for comp in complements]
    shortened_dnf = "+".join(sorted(dnf_terms))
    
    # Build matrix C using pandas
    C = pd.DataFrame(0, index=vertex_labels, columns=range(1, len(maximal_independent_sets) + 1))
    for j, mis in enumerate(maximal_independent_sets, 1):
        for v in mis:
            C.loc[v, j] = 1
    
    return formula_pg, shortened_dnf, maximal_independent_sets, C

def find_minimal_covering(maximal_independent_sets, all_vertices):
    all_vertices_set = set(all_vertices)
    s = len(maximal_independent_sets)
    for k in range(1, s + 1):
        for comb in combinations(range(s), k):
            selected_sets = [set(maximal_independent_sets[i]) for i in comb]
            union = set().union(*selected_sets)
            if union == all_vertices_set:
                return k, [maximal_independent_sets[i] for i in comb]
    return None, None

def get_predefined_graph():
    edges = [
        ('a', 'b'), ('a', 'c'), ('b', 'c'), ('b', 'e'), ('b', 'g'),
        ('c', 'e'), ('c', 'f'), ('d', 'e'), ('d', 'f'), ('d', 'g')
    ]
    return edges, 7

# Main program
n = int(input("Использовать заранее заданный граф? (1 - да, 0 - нет): "))
if n == 0:
    num_vertices = int(input("Введите количество вершин: "))
    edges = []
    for i in range(num_vertices):
        edge_input = input(f"Введите рёбра для вершины {i + 1} (формат: 'u v', 'u' - начальная, 'v' - конечная, или '0' для завершения): ")
        if edge_input == "0":
            break
        u, v = edge_input.split()
        edges.append((u, v))
else:
    edges, num_vertices = get_predefined_graph()
    vertex_labels = list(string.ascii_lowercase)[:num_vertices]
if not edges:
    print("Граф пустой, анализ невозможен!")
else:
    formula_pg, shortened_dnf, maximal_independent_sets, C = magu_weisman_algorithm(edges, num_vertices)
    
    print("### Шаг 1: Исходная формула Πg")
    print(formula_pg)
    print("\n### Шаг 2: Сокращённая ДНФ формулы Πg")
    print(shortened_dnf)
    
    print("\n### Шаг 3: Все максимальные ВУМ")
    for i, mis in enumerate(maximal_independent_sets, 1):
        print(f"F{i} = {{{','.join(mis)}}}")
    
    print("\n### Шаг 4: Матрица C")
    print(C.to_string())
    
    # Step 5: Find chromatic number and minimal covering
    k, covering = find_minimal_covering(maximal_independent_sets, vertex_labels)
    if k is not None:
        print(f"\n### Шаг 5: Хроматическое число χ(G) = {k}")
        print("Один из вариантов минимального покрытия:")
        for i, mis in enumerate(covering, 1):
            print(f"Цвет {i}: {{{','.join(mis)}}}")
        
        # Step 6: Assign colors
        color_assignment = {}
        for v in vertex_labels:
            for i, mis in enumerate(covering, 1):
                if v in mis:
                    color_assignment[v] = i
                    break  # Assign the first color found
        
        print("\n### Шаг 6: Раскраска вершин")
        for v in sorted(color_assignment.keys()):
            print(f"Вершина {v}: цвет {color_assignment[v]}")
    else:
        print("Не удалось найти покрытие.")