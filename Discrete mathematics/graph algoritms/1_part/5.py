import pandas as pd

# ANSI-коды для цветного текста
BLUE = "\033[94m"
RESET = "\033[0m"

def find(parent, i):
    if parent[i] != i:
        parent[i] = find(parent, parent[i])
    return parent[i]

def union(parent, rank, x, y):
    if rank[x] < rank[y]:
        parent[x] = y
    elif rank[x] > rank[y]:
        parent[y] = x
    else:
        parent[y] = x
        rank[x] += 1

def kruskal_mst(graph, V):
    m_star = 0
    S = 0
    X_star = [{i} for i in range(V)]
    
    graph = sorted(graph, key=lambda item: item[2])
    
    parent = [node for node in range(V)]
    rank = [0] * V
    
    step = 1
    j = 0
    
    # Таблица R
    print("На первом этапе формируем таблицу R:")
    table_data = {
        "№": list(range(1, len(graph) + 1)),
        "Ребро": [f"{chr(97 + u)}-{chr(97 + v)}" for u, v, _ in graph],
        "Вес": [w for _, _, w in graph]
    }
    df_R = pd.DataFrame(table_data)
    print("Таблица R (отсортированные рёбра):")
    print(df_R.to_string(index=False))
    print(f"\nm* = {m_star}")
    print(f"S = {S}")
    print(f"X* = {[{chr(97 + x) for x in subset} for subset in X_star]}\n")
    
    print("На втором этапе выполняем следующие действия:\n")
    
    steps_data = {
        "Шаг": [],
        "Ребро": [],
        "Вес": [],
        "Статус": [],
        "m*": [],
        "S": [],
        "X*": []
    }
    
    while m_star < V - 1 and j < len(graph):
        u, v, w = graph[j]
        u_letter = chr(97 + u)
        v_letter = chr(97 + v)
        
        steps_data["Шаг"].append(step)
        steps_data["Ребро"].append(f"{u_letter}-{v_letter}")
        steps_data["Вес"].append(w)
        
        x = find(parent, u)
        y = find(parent, v)
        
        u_in = set()
        v_in = set()
        for idx, subset in enumerate(X_star):
            if u in subset:
                u_in = subset
            if v in subset:
                v_in = subset
        
        if u_in != v_in:
            status = f"{BLUE}Дуга входит в МОД{RESET}"
            m_star += 1
            S += w
            union(parent, rank, x, y)
            
            new_subset = u_in.union(v_in)
            X_star = [subset for subset in X_star if subset != u_in and subset != v_in]
            X_star.append(new_subset)
        else:
            status = "Ребро пропущено"
        
        steps_data["Статус"].append(status)
        steps_data["m*"].append(m_star)
        steps_data["S"].append(S)
        steps_data["X*"].append(str([{chr(97 + x) for x in subset} for subset in X_star]))
        
        j += 1
        step += 1
    
    df_steps = pd.DataFrame(steps_data)
    print("Таблица шагов выполнения:")
    print(df_steps.to_string(index=False))
    
    print("\nЦикл закончен.")
    print(f"МОД с суммарным весом рёбер S = {S} построено.")
    
    print("\nРёбра в минимальном остовном дереве:")
    result = []
    j = 0
    m_star = 0
    parent = [node for node in range(V)]
    rank = [0] * V
    graph = sorted(graph, key=lambda item: item[2])
    
    final_mst_data = {
        "Ребро": [],
        "Вес": []
    }
    
    while m_star < V - 1 and j < len(graph):
        u, v, w = graph[j]
        x = find(parent, u)
        y = find(parent, v)
        if x != y:
            m_star += 1
            u_letter = chr(97 + u)
            v_letter = chr(97 + v)
            final_mst_data["Ребро"].append(f"{u_letter}-{v_letter}")
            final_mst_data["Вес"].append(w)
            union(parent, rank, x, y)
        j += 1
    
    df_mst = pd.DataFrame(final_mst_data)
    print(df_mst.to_string(index=False))

# Ввод данных
print("Введите количество вершин (максимум 26):")
V = int(input())
if V > 26:
    print("Ошибка: поддерживается максимум 26 вершин (a-z)")
    exit()

print("Доступные вершины:", " ".join(chr(97 + i) for i in range(V)))
print("Введите количество рёбер:")
E = int(input())

graph = []
print("Вводите рёбра в формате 'вершина1 вершина2 вес' (например, 'a b 4'):")
for _ in range(E):
    try:
        input_str = input().split()
        if len(input_str) != 3:
            print("Ошибка: введите две вершины и вес через пробел")
            continue
            
        u_str, v_str, w_str = input_str
        w = int(w_str)
        
        if len(u_str) != 1 or len(v_str) != 1:
            print("Ошибка: используйте одиночные буквы для вершин")
            continue
            
        u = ord(u_str.lower()) - 97
        v = ord(v_str.lower()) - 97
        
        if u >= V or v >= V or u < 0 or v < 0:
            print("Ошибка: используйте вершины из диапазона a-", chr(96 + V))
            continue
            
        graph.append([u, v, w])
    except ValueError:
        print("Ошибка: вес должен быть числом")
        continue
    except:
        print("Ошибка ввода")
        continue

# Запуск алгоритма
if graph:
    kruskal_mst(graph, V)
else:
    print("Граф пустой")