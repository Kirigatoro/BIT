import math
import pandas as pd  # type: ignore

def print_matrix(matrix, title="Матрица весов"):
    print(f"\n{title}:")
    n = len(matrix)
    print("   " + "  ".join(f"{i+1:>3}" for i in range(n)))
    for i, row in enumerate(matrix):
        formatted_row = "  ".join(f"{val if val != math.inf else '∞':>3}" for val in row)
        print(f"{i+1:>2} {formatted_row}")

def reconstruct_path(predecessor, start, end):
    path = []
    current = end
    while current is not None:
        path.append(current + 1)
        current = predecessor[current]
    path.reverse()
    return path

def calculate_path_weight(matrix, path):
    weight = 0
    for i in range(len(path) - 1):
        u = path[i] - 1
        v = path[i + 1] - 1
        weight += matrix[u][v]
    return weight

def calculate_path_length(path):
    return len(path) - 1

def input_graph():
    n = int(input("Введите количество вершин: "))
    mat = [[math.inf] * n for _ in range(n)]
    print("Введите рёбра в формате 'откуда куда вес'. Для завершения введите 'done'.")
    while True:
        line = input()
        if line.lower() == "done":
            break
        try:
            u, v, w = map(float, line.split())
            u, v = int(u) - 1, int(v) - 1
            mat[u][v] = w
        except ValueError:
            print("Ошибка ввода! Введите три числа: откуда, куда, вес.")
    return mat

default_mat = [
    [math.inf,        5,        2,        5,       12, math.inf],
    [math.inf, math.inf, math.inf, math.inf, math.inf,        2],
    [math.inf,        2, math.inf,        1, math.inf, math.inf],
    [math.inf, math.inf, math.inf, math.inf, math.inf,        2],
    [math.inf, math.inf, math.inf, math.inf, math.inf, math.inf],
    [math.inf, math.inf, math.inf, math.inf,        2, math.inf]]

choice = input("Использовать предопределённый граф? (y/n): ").strip().lower()
mat = input_graph() if choice == "n" else default_mat
n = len(mat)
start = int(input(f"Введите стартовую вершину (1-{n}): ")) - 1
end = int(input(f"Введите конечную вершину (1-{n}): ")) - 1

print_matrix(mat, "Матрица весов (W)")
dist = [math.inf] * n
predecessor = [None] * n
dist[start] = 0
lambda_steps = [dist.copy()]

for step in range(n - 1):
    print(f"\nРелаксация при шаге L ≤ {step + 1}")
    updated = False
    prev_dist = dist.copy()  # Копия dist на начало шага
    for v in range(n):
        if v == start:  # Пропускаем стартовую вершину
            continue
        if step == 0:
            u_range = [start]  # Только стартовая вершина
        else:
            u_range = range(n)  # Все вершины

        for u in u_range:
            if mat[u][v] != math.inf and prev_dist[u] != math.inf:
                new_dist = prev_dist[u] + mat[u][v]
                print(f"Проверяем вершину x{v+1} через x{u+1}: λ^{step+1}(x{v+1}) = min(λ^{step}(x{v+1}), λ^{step}(x{u+1}) + w(x{u+1}, x{v+1}))")
                print(f"λ^{step+1}(x{v+1}) = min({dist[v] if dist[v] != math.inf else '∞'}, {prev_dist[u]} + {mat[u][v]}) = {new_dist if new_dist < dist[v] else dist[v]}")
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    predecessor[v] = u
                    updated = True
    
    lambda_steps.append(dist.copy())
    # Проверяем, изменилась ли лямбда по сравнению с предыдущим шагом
    if dist == prev_dist:
        print("Лямбда не изменилась, завершаем релаксацию.")
        break
    if not updated:
        print("Обновлений не произошло.")

# Проверка на отрицательные циклы
for v in range(n):
    for u in range(n):
        if mat[u][v] != math.inf and dist[u] != math.inf and dist[u] + mat[u][v] < dist[v]:
            print("Граф содержит отрицательный цикл!")
            break

df_lambda_steps = pd.DataFrame(lambda_steps).T
df_lambda_steps.columns = [f"Шаг {i}" for i in range(len(lambda_steps))]
df_lambda_steps.index = [f"x{i+1}" for i in range(n)]
print("\nТаблица лямбда (λ) по шагам релаксации (инвертированная):")
print(df_lambda_steps)

path = reconstruct_path(predecessor, start, end)
path_weight = calculate_path_weight(mat, path)
path_length = calculate_path_length(path)
print(f"\nКратчайший путь от {start+1} до {end+1}: {' -> '.join(map(str, path))}")
print(f"Длина пути (количество рёбер): {path_length}")
print(f"Вес пути (сумма весов рёбер): {path_weight}")