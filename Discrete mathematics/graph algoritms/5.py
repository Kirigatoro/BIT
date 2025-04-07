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

# Ввод данных (задаём напрямую для примера)
V = 6  # Вершины: a, b, c, d, e, f
graph = [
    [0, 1, 25],  # a-b
    [0, 2, 10],  # a-c
    [0, 3, 23],  # a-d
    [0, 5, 22],  # a-f
    [1, 3, 15],  # b-d
    [1, 4, 6],   # b-e
    [2, 3, 16],  # c-d
    [2, 4, 5],   # c-e
    [2, 5, 24]   # c-f
]

# Запуск алгоритма
kruskal_mst(graph, V)