import pandas as pd

def create_adjacency_matrix(table):
    """
    Преобразует таблицу смежности в матрицу смежности и возвращает её как DataFrame.
    """
    # Получаем уникальные вершины
    vertices = sorted(set(row[0] for row in table))
    vertex_count = len(vertices)
    vertex_indices = {vertex: i for i, vertex in enumerate(vertices)}

    # Инициализируем матрицу нулями
    matrix = [[0] * vertex_count for _ in range(vertex_count)]

    # Заполняем матрицу на основе таблицы
    for row in table:
        source = vertex_indices[row[0]]
        for target in row[1:]:
            if target in vertex_indices:
                matrix[source][vertex_indices[target]] = 1

    # Создаем DataFrame
    df = pd.DataFrame(matrix, index=vertices, columns=vertices)
    return df, vertex_indices

def print_matrix(df):
    """
    Выводит матрицу смежности в читаемом виде.
    """
    print("\nМатрица смежности графа:")
    print(df.to_string())

def is_safe_to_add(vertex, matrix, path, position):
    """
    Проверяет, можно ли добавить вершину в текущий путь.
    """
    # Нет ребра от предыдущей вершины к текущей
    if matrix.iloc[path[position - 1], vertex] == 0:
        return False
    # Вершина уже есть в пути
    if vertex in path[:position]:
        return False
    return True

def find_all_hamiltonian_cycles(matrix, vertex_count, path, position, all_cycles):
    """
    Рекурсивно ищет все гамильтоновы циклы в графе.
    """
    # Если все вершины посещены
    if position == vertex_count:
        # Проверяем, есть ли ребро от последней вершины к первой
        if matrix.iloc[path[position - 1], path[0]] == 1:
            cycle = [matrix.index[vertex] for vertex in path] + [matrix.index[path[0]]]
            all_cycles.append(cycle)
        return

    # Перебираем все вершины
    for vertex in range(vertex_count):
        if is_safe_to_add(vertex, matrix, path, position):
            path[position] = vertex
            find_all_hamiltonian_cycles(matrix, vertex_count, path, position + 1, all_cycles)
            path[position] = -1  # Откатываем для поиска других решений

def find_hamiltonian_cycles(matrix):
    """
    Основная функция для поиска и вывода всех гамильтоновых циклов.
    """
    vertex_count = len(matrix)
    path = [-1] * vertex_count
    path[0] = 0  # Начинаем с первой вершины
    all_cycles = []

    find_all_hamiltonian_cycles(matrix, vertex_count, path, 1, all_cycles)

    if not all_cycles:
        print("\nГамильтонов цикл не существует")
        return None

    print("\nВсе гамильтоновы циклы:")
    for number, cycle in enumerate(all_cycles, 1):
        print(f"Цикл {number}: {' -> '.join(cycle)}")
    return all_cycles

# Пример таблицы смежности
table = [
    ['a', 'b'],
    ['b', 'c', 'e'],
    ['c', 'a', 'd'],
    ['d', 'c', 'f'],
    ['e', 'c', 'd'],
    ['f', 'a', 'b', 'c']
]

# Запуск программы
graph_matrix, indices = create_adjacency_matrix(table)
print_matrix(graph_matrix)
find_hamiltonian_cycles(graph_matrix)