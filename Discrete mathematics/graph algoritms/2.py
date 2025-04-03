import math
import pandas as pd  # type: ignore

def print_matrix(matrix, title="Матрица весов"):
    """Функция для красивого вывода матрицы"""
    print(f"\n{title}:")
    n = len(matrix)
    print("   " + "  ".join(f"{i+1:>3}" for i in range(n)))  # Заголовок столбцов
    for i, row in enumerate(matrix):
        formatted_row = "  ".join(f"{val if val != math.inf else '∞':>3}" for val in row)
        print(f"{i+1:>2} {formatted_row}")

def reconstruct_path(predecessor, start, end):
    """Функция для восстановления маршрута"""
    path = []
    current = end
    while current is not None:
        path.append(current + 1)  # +1, чтобы вернуть индексацию в нормальный вид
        current = predecessor[current]
    path.reverse()
    return path

def input_graph():
    """Функция для ввода графа с клавиатуры"""
    n = int(input("Введите количество вершин: "))
    mat = [[math.inf] * n for _ in range(n)]
    
    print("Введите рёбра в формате 'откуда куда вес'. Для завершения введите 'done'.")
    
    while True:
        line = input()
        if line.lower() == "done":
            break
        try:
            u, v, w = map(float, line.split())
            u, v = int(u) - 1, int(v) - 1  # Переключение на индексы
            mat[u][v] = w
        except ValueError:
            print("Ошибка ввода! Введите три числа: откуда, куда, вес.")

    return mat

# Предопределённая матрица весов (из изображения)
default_mat = [
    [math.inf,        5,        2,        5,       12, math.inf],
    [math.inf, math.inf, math.inf, math.inf, math.inf,        2],
    [math.inf,        2, math.inf,        1, math.inf, math.inf],
    [math.inf, math.inf, math.inf, math.inf, math.inf,        2],
    [math.inf, math.inf, math.inf, math.inf, math.inf, math.inf],
    [math.inf, math.inf, math.inf, math.inf,        2, math.inf]
]

# Запрос на ввод графа
choice = input("Использовать предопределённый граф? (y/n): ").strip().lower()
mat = input_graph() if choice == "n" else default_mat

# Количество вершин
n = len(mat)

# Ввод стартовой и конечной вершины
start = int(input(f"Введите стартовую вершину (1-{n}): ")) - 1
end = int(input(f"Введите конечную вершину (1-{n}): ")) - 1

# Вывод матрицы весов
print_matrix(mat, "Матрица весов (W)")

# Инициализация расстояний и предков
dist = [math.inf] * n
predecessor = [None] * n  # Хранит предшественника для каждой вершины
dist[start] = 0

# Список рёбер
edges = [(u, v, mat[u][v]) for u in range(n) for v in range(n) if mat[u][v] != math.inf]

# Список для хранения шагов релаксации
lambda_steps = []

# Алгоритм Форда-Беллмана с сохранением промежуточных состояний
for _ in range(n - 1):
    for u, v, w in edges:
        if dist[u] != math.inf and dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
            predecessor[v] = u  # Запоминаем, откуда пришли
    lambda_steps.append(dist.copy())  # Сохраняем текущее состояние

# Проверка на отрицательные циклы
for u, v, w in edges:
    if dist[u] != math.inf and dist[u] + w < dist[v]:
        print("Граф содержит отрицательный цикл!")
        break

# Создание DataFrame с шагами релаксации
df_lambda_steps = pd.DataFrame(lambda_steps, columns=[f"x{i+1}" for i in range(n)])
df_lambda_steps.index = [f"Шаг {i+1}" for i in range(len(lambda_steps))]

print("\nТаблица лямбда (λ) по шагам релаксации:")
print(df_lambda_steps.T)

# Восстановление маршрута
if dist[end] == math.inf:
    print(f"Из вершины {start+1} в вершину {end+1} пути нет.")
else:
    path = reconstruct_path(predecessor, start, end)
    print(f"\nКратчайший путь из {start+1} в {end+1}: {' → '.join(map(str, path))}")
    print(f"Длина пути: {len(path) - 1}")
    print(f"Вес пути: {dist[end]}")