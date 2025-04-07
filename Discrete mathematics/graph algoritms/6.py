import pandas as pd
from itertools import combinations
import string

def magu_weisman_algorithm(edges, num_vertices):
    vertex_labels = list(string.ascii_lowercase)[:num_vertices]
    label_to_idx = {label: idx + 1 for idx, label in enumerate(vertex_labels)}
    edges_numeric = [(label_to_idx[u], label_to_idx[v]) for u, v in edges]
    
    # Шаг 1: Построение исходной формулы Πg (без пробелов, строчные буквы, сортировка)
    sorted_edges = sorted(edges, key=lambda x: (x[0], x[1]))
    formula_pg = "*".join([f"({u}+{v})" for u, v in sorted_edges])
    
    # Шаг 2-3: Нахождение всех максимальных ВУМ
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
    
    # Нахождение дополнений до максимальных ВУМ
    complements = [sorted(list(all_vertices - set(mis))) for mis in maximal_independent_sets]
    
    # Формирование сокращенной ДНФ (без пробелов, строчные буквы, сортировка)
    dnf_terms = ["".join(comp) for comp in complements]
    shortened_dnf = "+".join(sorted(dnf_terms))  # Сортировка лексикографически
    
    # Шаги 4-5: Максимальные ВУМ уже найдены
    mis_sizes = [len(mis) for mis in maximal_independent_sets]
    alpha_0 = max(mis_sizes) if mis_sizes else 0
    largest_mis = [mis for mis in maximal_independent_sets if len(mis) == alpha_0] if mis_sizes else []
    
    # Форматирование результатов в pandas DataFrame
    df_complements = pd.DataFrame({
        '№': range(1, len(complements) + 1),
        'Дополнение до максимального ВУМ': [f"{{{','.join(comp)}}}" for comp in complements],
        'Максимальное ВУМ': [f"{{{','.join(mis)}}}" for mis in maximal_independent_sets],
        'Мощность ВУМ': mis_sizes
    }) if complements else pd.DataFrame(columns=['№', 'Дополнение до максимального ВУМ', 'Максимальное ВУМ', 'Мощность ВУМ'])
    
    return formula_pg, shortened_dnf, df_complements, largest_mis, alpha_0

def get_graph_from_console():
    while True:
        try:
            num_vertices = int(input("Введите количество вершин графа (n, max 26): "))
            if 0 < num_vertices <= 26:
                break
            else:
                print("Количество вершин должно быть от 1 до 26!")
        except ValueError:
            print("Пожалуйста, введите целое число!")
    
    vertex_labels = list(string.ascii_lowercase)[:num_vertices]
    print(f"Доступные вершины: {', '.join(vertex_labels)}")
    print("Введите ребра графа в формате 'u v' (например, 'a c').")
    print("Для завершения ввода введите пустую строку.")
    
    edges = []
    valid_vertices = set(vertex_labels)
    while True:
        edge_input = input("Введите ребро (или нажмите Enter для завершения): ").strip().lower()
        if not edge_input:
            break
        try:
            u, v = edge_input.split()
            if u not in valid_vertices or v not in valid_vertices:
                print(f"Вершины должны быть из списка: {', '.join(vertex_labels)}!")
                continue
            if u == v:
                print("Петли не допускаются!")
                continue
            edges.append((u, v))
        except ValueError:
            print("Неверный формат! Введите две буквы, разделенные пробелом.")
    
    return edges, num_vertices

# Основная программа
print("Программа для поиска наибольших ВУМ по алгоритму Магу-Вейсмана")
edges, num_vertices = get_graph_from_console()

if not edges:
    print("Граф пустой, анализ невозможен!")
else:
    formula_pg, shortened_dnf, df_results, largest_mis, alpha_0 = magu_weisman_algorithm(edges, num_vertices)
    print("\nИсходная формула Πg:")
    print(formula_pg)
    print("\nСокращенная дизъюнктивная нормальная форма записи формулы Πg:")
    print(shortened_dnf)
    print("\nВсе максимальные ВУМ и их дополнения:")
    print(df_results.to_string(index=False))
    print("\nНаибольшие ВУМ:")
    for i, mis in enumerate(largest_mis, 1):
        print(f"F{i} = {{{','.join(mis)}}}")
    print(f"Число внутренней устойчивости α₀(G) = {alpha_0}")