import pandas as pd

def input_adjacency_table():
    while True:
        try:
            vertex_count = int(input("Введите количество вершин: "))
            if vertex_count <= 0:
                print("Количество вершин должно быть положительным числом.")
                continue
            break
        except ValueError:
            print("Пожалуйста, введите целое число.")

    vertices = [chr(97 + i) for i in range(vertex_count)]  # a, b, c, ...
    table = []

    print("Введите смежные вершины для каждой вершины (через пробел, например: b c).")
    print("Если дуг нет, просто нажмите Enter.")
    for vertex in vertices:
        while True:
            edges = input(f"Смежные вершины для {vertex}: ").strip().lower().split()
            if all(edge in vertices or edge == '' for edge in edges):
                table.append([vertex] + edges)
                break
            else:
                print(f"Ошибка: используйте только вершины из {vertices}.")
    return table

def create_adjacency_matrix(table):
    vertices = sorted(set(row[0] for row in table))
    vertex_count = len(vertices)
    vertex_indices = {vertex: i for i, vertex in enumerate(vertices)}
    matrix = [[0] * vertex_count for _ in range(vertex_count)]
    for row in table:
        source = vertex_indices[row[0]]
        for target in row[1:]:
            if target in vertex_indices:
                matrix[source][vertex_indices[target]] = 1
    df = pd.DataFrame(matrix, index=vertices, columns=vertices)
    return df, vertex_indices

def print_matrix(df):
    print("\nМатрица смежности графа:")
    print(df.to_string())

def is_safe_to_add(vertex, matrix, path, position):
    if matrix.iloc[path[position - 1], vertex] == 0:
        return False
    if vertex in path[:position]:
        return False
    return True

def print_step(action, vertex, path, matrix):
    name = matrix.index[vertex]
    current_path = " -> ".join([matrix.index[v] for v in path if v != -1])
    if action == "add":
        print(f"Добавили вершину {name} | {current_path}")
    elif action == "remove":
        print(f"Удалили вершину {name}")

def find_all_hamiltonian_cycles(matrix, vertex_count, path, position, all_cycles):
    if position == vertex_count:
        if matrix.iloc[path[position - 1], path[0]] == 1:
            cycle = [matrix.index[v] for v in path] + [matrix.index[path[0]]]
            all_cycles.append(cycle)
            print("\nНайден гамильтонов цикл:")
            print(f"\033[3m\033[34m{' -> '.join(cycle)}\033[0m")  # курсив и синий
        return

    for vertex in range(vertex_count):
        if is_safe_to_add(vertex, matrix, path, position):
            path[position] = vertex
            print_step("add", vertex, path, matrix)
            find_all_hamiltonian_cycles(matrix, vertex_count, path, position + 1, all_cycles)
            print_step("remove", vertex, path, matrix)
            path[position] = -1

def find_hamiltonian_cycles(matrix):
    vertex_count = len(matrix)
    path = [-1] * vertex_count
    path[0] = 0  # начинаем с первой вершины (a)
    all_cycles = []

    print(f"\nСтартуем с вершины {matrix.index[0]}")
    find_all_hamiltonian_cycles(matrix, vertex_count, path, 1, all_cycles)

    if not all_cycles:
        print("\nГамильтонов цикл не существует.")
    else:
        print(f"\nВсего найдено {len(all_cycles)} гамильтоновых циклов.")
    return all_cycles

# ▶ Запуск программы
if __name__ == "__main__":
    table = input_adjacency_table()
    graph_matrix, indices = create_adjacency_matrix(table)
    print_matrix(graph_matrix)
    find_hamiltonian_cycles(graph_matrix)