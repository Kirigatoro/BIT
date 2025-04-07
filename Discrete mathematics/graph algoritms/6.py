import pandas as pd
from itertools import product

def magu_weisman_algorithm(edges, num_vertices):
    # Шаг 1: Построение исходной формулы Πg
    vertices = list(range(1, num_vertices + 1))
    formula_pg = " * ".join([f"(x{u}+x{v})" for u, v in edges])
    
    # Шаг 2-3: Нахождение дополнений до максимальных ВУМ
    formula_terms = [(f"x{u}", f"x{v}") for u, v in edges]
    
    def generate_combinations(terms):
        result = []
        for combination in product([0, 1], repeat=len(terms)):
            current_term = []
            valid = True
            for i, (choice, (x1, x2)) in enumerate(zip(combination, terms)):
                if choice == 0:
                    current_term.append(x1[1:])  # Номер вершины без 'x'
                else:
                    current_term.append(x2[1:])
                # Проверка на отсутствие смежных вершин
                for j in range(len(current_term)):
                    for k in range(j + 1, len(current_term)):
                        if (int(current_term[j]), int(current_term[k])) in edges or \
                           (int(current_term[k]), int(current_term[j])) in edges:
                            valid = False
                            break
                    if not valid:
                        break
                if not valid:
                    break
            if valid and current_term:
                result.append(sorted(list(set(current_term))))
        return result

    complements = generate_combinations(formula_terms)
    
    # Формирование сокращенной ДНФ
    shortened_dnf = " + ".join(["".join([f"x{v}" for v in comp]) for comp in complements])
    
    # Шаги 4-5: Определение максимальных ВУМ
    maximal_independent_sets = []
    for comp in complements:
        comp_set = set(int(x) for x in comp)
        mis = sorted(list(set(vertices) - comp_set))
        maximal_independent_sets.append(mis)
    
    # Шаг 6: Определение наибольших ВУМ и α₀(G)
    mis_sizes = [len(mis) for mis in maximal_independent_sets]
    alpha_0 = max(mis_sizes)
    largest_mis = [mis for mis in maximal_independent_sets if len(mis) == alpha_0]
    
    # Форматирование результатов в pandas DataFrame
    df_complements = pd.DataFrame({
        '№': range(1, len(complements) + 1),
        'Дополнение до максимального ВУМ': [f"{{{','.join(map(str, comp))}}}" for comp in complements],
        'Максимальное ВУМ': [f"{{{','.join(map(str, mis))}}}" for mis in maximal_independent_sets],
        'Мощность ВУМ': mis_sizes
    })
    
    return formula_pg, shortened_dnf, df_complements, largest_mis, alpha_0

def get_graph_from_console():
    # Ввод количества вершин
    while True:
        try:
            num_vertices = int(input("Введите количество вершин графа (n): "))
            if num_vertices > 0:
                break
            else:
                print("Количество вершин должно быть положительным числом!")
        except ValueError:
            print("Пожалуйста, введите целое число!")
    
    # Ввод ребер
    edges = []
    print("Введите ребра графа в формате 'u v' (например, '1 3'), где u и v — номера вершин.")
    print("Для завершения ввода введите пустую строку.")
    
    while True:
        edge_input = input("Введите ребро (или нажмите Enter для завершения): ").strip()
        if not edge_input:
            break
        try:
            u, v = map(int, edge_input.split())
            if u < 1 or v < 1 or u > num_vertices or v > num_vertices:
                print(f"Вершины должны быть в диапазоне от 1 до {num_vertices}!")
                continue
            if u == v:
                print("Петли не допускаются!")
                continue
            edges.append((u, v))
        except ValueError:
            print("Неверный формат! Введите два числа, разделенных пробелом.")
    
    return edges, num_vertices

# Основная программа
print("Программа для поиска наибольших ВУМ по алгоритму Магу-Вейсмана")
edges, num_vertices = get_graph_from_console()

if not edges:
    print("Граф пустой, анализ невозможен!")
else:
    # Выполнение алгоритма
    formula_pg, shortened_dnf, df_results, largest_mis, alpha_0 = magu_weisman_algorithm(edges, num_vertices)

    # Вывод результатов
    print("\nИсходная формула Πg:")
    print(formula_pg)
    print("\nСокращенная дизъюнктивная нормальная форма записи формулы Πg:")
    print(shortened_dnf)
    print("\nВсе максимальные ВУМ и их дополнения:")
    print(df_results.to_string(index=False))
    print("\nНаибольшие ВУМ:")
    for i, mis in enumerate(largest_mis, 1):
        print(f"F{i} = {{{','.join(map(str, mis))}}}")
    print(f"Число внутренней устойчивости α₀(G) = {alpha_0}")