import pandas as pd
import string
import math  # Для использования math.inf вместо 10000

# Создаем список букв английского алфавита
letters = list(string.ascii_lowercase)

count_of_dots = 7
digit_to_letter = {i + 1: letters[i] for i in range(count_of_dots)}

# Матрица смежности (10000 заменены на math.inf)
mat = [
    [math.inf, 4.0,    math.inf, math.inf, math.inf, math.inf, math.inf],
    [math.inf, math.inf, math.inf, math.inf, 4.5,    math.inf, math.inf],
    [math.inf, math.inf, math.inf, math.inf, math.inf, math.inf, math.inf],
    [math.inf, 7.5,    math.inf, math.inf, 3.5,    math.inf, 4.5],
    [6,       math.inf, 3.5,    math.inf, math.inf, 6.5,    math.inf],
    [math.inf, math.inf, math.inf, math.inf, math.inf, math.inf, math.inf],
    [math.inf, math.inf, math.inf, math.inf, 0,      math.inf, math.inf]
]

# Создаем DataFrame с названиями столбцов и индексов 'a'-'g'
df = pd.DataFrame(mat, 
                 index=["a", "b", "c", "d", "e", "f", "g"], 
                 columns=["a", "b", "c", "d", "e", "f", "g"])
print("Матрица смежности:")
print(df)

# Начальные значения λ
l0 = [math.inf, math.inf, math.inf, 0, math.inf, math.inf, math.inf]

lambd = pd.DataFrame(l0, 
                    index=["a", "b", "c", "d", "e", "f", "g"], 
                    columns=[0])
print("\nНачальные значения λ:")
print(lambd)

flag = 5  # Количество итераций
counter = 0
print()

while flag > 0:
    print(f"\033[34m>>>>>>>>>>>>>>>>>>>> Релаксация при {counter+1} шаге\033[0m")
    pred = lambd[counter].tolist()
    tec = l0.copy()  # Создаем копию, чтобы не изменять исходный список
    
    for i in range(count_of_dots):
        if i == 3:  # Для вершины 'd' значение всегда 0
            tec[i] = 0
        else:
            # Берем столбец, соответствующий текущей вершине
            current_vertex = letters[i]
            now = df[current_vertex].tolist()
            print(f"\nРасчет для вершины {current_vertex.upper()}: {now}")
            
            minimum = math.inf
            for j in range(count_of_dots):
                if now[j] != math.inf:
                    new_min = min(pred[j] + now[j], pred[i])
                    print(f"min(λ[{j}] + w, λ[{i}]) = min({pred[j]} + {now[j]}, {pred[i]}) = {new_min}")
                    if new_min < minimum:
                        minimum = new_min
            print(f"Итоговый минимум для {current_vertex.upper()}: {minimum}")
            tec[i] = minimum
    
    lambd[counter+1] = tec
    print("\nРезультат после итерации:")
    print(lambd)
    
    counter += 1
    flag -= 1

print("\nФинальная таблица λ:")
print(lambd)