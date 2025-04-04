import pandas as pd

def input_adjacency_table():
    """
    Запрашивает таблицу смежности у пользователя через терминал.
    """
    # Запрашиваем количество вершин
    while True:
        try:
            vertex_count = int(input("Введите количество вершин: "))
            if vertex_count <= 0:
                print("Количество вершин должно быть положительным числом.")
                continue
            break
        except ValueError:
            print("Пожалуйста, введите целое число.")

    # Создаем список вершин (a, b, c, ...)
    vertices = [chr(97 + i) for i in range(vertex_count)]  # a=97 в ASCII
    table = []

    # Запрашиваем дуги для каждой вершины
    print("Введите смежные вершины для каждой вершины (через пробел, например: b c).")
    print("Если дуг нет, просто нажмите Enter.")
    for vertex in vertices:
        while True:
            edges = input(f"Смежные вершины для {vertex}: ").strip().split()
            # Проверяем, что введенные вершины корректны
            if all(edge in vertices or not edge for edge in edges):
                table.append([vertex] + edges)
                break
            else:
                print(f"Ошибка: используйте только вершины из {vertices}.")

    return table

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

def find_all_hamiltonian_cycles(matrix, vertex_count, path, position, all_cycles, steps, cycle_steps):
    """
    Рекурсивно ищет все гамильтоновы циклы и записывает шаги их построения.
    """
    # Если все вершины посещены
    if position == vertex_count:
        # Проверяем, есть ли ребро от последней вершины к первой
        if matrix.iloc[path[position - 1], path[0]] == 1:
            cycle = [matrix.index[vertex] for vertex in path] + [matrix.index[path[0]]]
            all_cycles.append(cycle)
            cycle_steps.append(steps[:])  # Сохраняем копию шагов для этого цикла
        return

    # Перебираем все вершины
    for vertex in range(vertex_count):
        if is_safe_to_add(vertex, matrix, path, position):
            path[position] = vertex
            current_path = [matrix.index[v] for v in path[:position + 1]]
            steps.append(f"Добавлена вершина {matrix.index[vertex]}, путь: {' -> '.join(current_path)}")
            find_all_hamiltonian_cycles(matrix, vertex_count, path, position + 1, all_cycles, steps, cycle_steps)
            path[position] = -1  # Откатываем для поиска других решений
            steps.pop()  # Убираем шаг добавления перед возвратом

def find_hamiltonian_cycles(matrix):
    """
    Основная функция для поиска и вывода всех гамильтоновых циклов с таблицей шагов.
    """
    vertex_count = len(matrix)
    path = [-1] * vertex_count
    path[0] = 0  # Начинаем с первой вершины
    all_cycles = []
    steps = [f"Начало с вершины {matrix.index[0]}"]
    cycle_steps = []  # Список шагов для каждого цикла

    find_all_hamiltonian_cycles(matrix, vertex_count, path, 1, all_cycles, steps, cycle_steps)

    if not all_cycles:
        print("\nГамильтонов цикл не существует")
        return None

    print("\nВсе гамильтоновы циклы:")
    for number, (cycle, cycle_step) in enumerate(zip(all_cycles, cycle_steps), 1):
        print(f"\nЦикл {number}: {' -> '.join(cycle)}")
        print(f"Таблица шагов для цикла {number}:")
        step_table = pd.DataFrame({
            "Шаг": range(1, len(cycle_step) + 1),
            "Действие": cycle_step
        })
        print(step_table.to_string(index=False))

    return all_cycles

# Запуск программы с вводом таблицы вручную
table = input_adjacency_table()
graph_matrix, indices = create_adjacency_matrix(table)
print_matrix(graph_matrix)
find_hamiltonian_cycles(graph_matrix)