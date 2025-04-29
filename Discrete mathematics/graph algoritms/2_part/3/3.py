import numpy as np
import pandas as pd
from collections import defaultdict
import os

def create_template_file(n, filename="graph_input.txt"):
    """Создание шаблона файла для ввода графа."""
    labels = [chr(97 + i) for i in range(n)]
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# Шаблон для ввода графа\n")
        f.write("# Количество вершин (n): указано в программе\n")
        f.write("# Формат:\n")
        f.write("# Для каждой вершины укажите дуги, ребра и петли.\n")
        f.write("# Дуги: vertex -> j количество_дуг (например, \"f 1\")\n")
        f.write("# Ребра: {vertex, j} количество_ребер (например, \"f 1\")\n")
        f.write("# Петли: количество_петель (например, \"1\")\n")
        f.write("# Если связей нет, оставьте пустую строку или напишите \"none\".\n")
        f.write("# Разделяйте секции пустой строкой.\n\n")

        for vertex in labels:
            f.write(f"[vertex {vertex}]\n")
            f.write("arcs: none\n")
            f.write("edges: none\n")
            f.write("loops: 0\n\n")



def save_graph_to_file(n, arcs, edges, loops, filename="graph_input.txt"):
    """Сохранение графа в файл в формате шаблона."""
    labels = [chr(97 + i) for i in range(n)]
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# Граф, введенный вручную\n")
        f.write("# Количество вершин (n): указано в программе\n")
        f.write("# Формат:\n")
        f.write("# Для каждой вершины указаны дуги, ребра и петли.\n")
        f.write("# Дуги: vertex -> j количество_дуг (например, \"f 1\")\n")
        f.write("# Ребра: {vertex, j} количество_ребер (например, \"f 1\")\n")
        f.write("# Петли: количество_петель (например, \"1\")\n")
        f.write("# Если связей нет, указано \"none\".\n")
        f.write("# Разделяйте секции пустой строкой.\n\n")

        for i in range(n):
            vertex = labels[i]
            f.write(f"[vertex {vertex}]\n")

            vertex_arcs = [f"{labels[j]} {count}" for (start, j), count in arcs.items() if start == i]
            if vertex_arcs:
                f.write(f"arcs: {'; '.join(vertex_arcs)}\n")
            else:
                f.write("arcs: none\n")

            vertex_edges = []
            for (u, v), count in edges.items():
                if u == i:
                    vertex_edges.append(f"{labels[v]} {count}")
                elif v == i:
                    vertex_edges.append(f"{labels[u]} {count}")
            if vertex_edges:
                f.write(f"edges: {'; '.join(vertex_edges)}\n")
            else:
                f.write("edges: none\n")

            loop_count = loops.get(i, 0)
            f.write(f"loops: {loop_count}\n\n")

def read_graph_from_file(n, filename="graph_input.txt"):
    """Чтение графа из текстового файла."""
    arcs = {}
    edges = {}
    loops = {}
    labels = [chr(97 + i) for i in range(n)]

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return None, None, None

    current_vertex = None
    processed_edges = set()

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        if line.startswith('[vertex'):
            vertex_label = line.split(' ')[1].strip(']')
            if vertex_label not in labels:
                print(f"Ошибка: вершина '{vertex_label}' не входит в диапазон {labels}.")
                continue
            current_vertex = labels.index(vertex_label)
        elif line.startswith('arcs:') and current_vertex is not None:
            data = line.split(':', 1)[1].strip()
            if data.lower() != 'none':
                for arc in data.split(';'):
                    arc = arc.strip()
                    if not arc:
                        continue
                    try:
                        j_label, count = arc.split()
                        count = int(count)
                        if j_label not in labels:
                            print(f"Ошибка в arcs для вершины {labels[current_vertex]}: вершина '{j_label}' не существует.")
                            continue
                        j = labels.index(j_label)
                        if current_vertex == j:
                            print(f"Ошибка в arcs для вершины {labels[current_vertex]}: дуга не может быть петлей.")
                            continue
                        if count <= 0:
                            print(f"Ошибка в arcs для вершины {labels[current_vertex]}: количество дуг должно быть положительным.")
                            continue
                        arcs[(current_vertex, j)] = count
                    except ValueError:
                        print(f"Ошибка в arcs для вершины {labels[current_vertex]}: неверный формат '{arc}'. Ожидается 'j количество'.")
        elif line.startswith('edges:') and current_vertex is not None:
            data = line.split(':', 1)[1].strip()
            if data.lower() != 'none':
                for edge in data.split(';'):
                    edge = edge.strip()
                    if not edge:
                        continue
                    try:
                        j_label, count = edge.split()
                        count = int(count)
                        if j_label not in labels:
                            print(f"Ошибка в edges для вершины {labels[current_vertex]}: вершина '{j_label}' не существует.")
                            continue
                        j = labels.index(j_label)
                        if current_vertex == j:
                            print(f"Ошибка в edges для вершины {labels[current_vertex]}: ребро не может быть петлей.")
                            continue
                        if count <= 0:
                            print(f"Ошибка в edges для вершины {labels[current_vertex]}: количество ребер должно быть положительным.")
                            continue
                        edge_key = (min(current_vertex, j), max(current_vertex, j))
                        if edge_key not in processed_edges:
                            edges[edge_key] = edges.get(edge_key, 0) + count
                            processed_edges.add(edge_key)
                    except ValueError:
                        print(f"Ошибка в edges для вершины {labels[current_vertex]}: неверный формат '{edge}'. Ожидается 'j количество'.")
        elif line.startswith('loops:') and current_vertex is not None:
            data = line.split(':', 1)[1].strip()
            if data != '0':
                try:
                    count = int(data)
                    if count <= 0:
                        print(f"Ошибка в loops для вершины {labels[current_vertex]}: количество петель должно быть положительным.")
                        continue
                    loops[current_vertex] = count
                except ValueError:
                    print(f"Ошибка в loops для вершины {labels[current_vertex]}: неверный формат '{data}'. Ожидается число.")

    return arcs, edges, loops

def input_graph(n):
    """Улучшенный ввод графа с цветным форматированием."""
    arcs = {}
    edges = {}
    loops = {}
    labels = [chr(97 + i) for i in range(n)]

    print(f"\nВвод графа с {n} вершинами (вершины: {', '.join(labels)}).")
    print("Для каждой вершины вводите связи с другими вершинами.")

    for i in range(n):
        vertex = labels[i]
        print(f"\033[1;31m\nВвод связей для вершины '{vertex}':\033[0m")

        print(f"\033[34mВвод дуг из '{vertex}' (направленные связи vertex -> j). Введите 'done' для завершения ввода дуг.\033[0m")
        while True:
            inp = input("Введите дугу (буква_вершины количество_дуг, например 'f 1') или 'done': ").strip().lower()
            if inp == 'done':
                break
            try:
                j_label, count = inp.split()
                count = int(count)
                if j_label not in labels:
                    print(f"Ошибка: вершина '{j_label}' не существует. Допустимые вершины: {', '.join(labels)}.")
                    continue
                j = labels.index(j_label)
                if i == j:
                    print("Дуга не может быть петлей (i == j). Используйте ввод петель для этого.")
                    continue
                if count <= 0:
                    print("Количество дуг должно быть положительным.")
                    continue
                arcs[(i, j)] = count
            except ValueError:
                print("Ошибка ввода. Формат: буква_вершины количество_дуг (например 'f 1').")

        print(f"\033[34m\nВвод ребер для '{vertex}' (ненаправленные связи {{vertex, j}}). Введите 'done' для завершения ввода ребер.\033[0m")
        while True:
            inp = input("Введите ребро (буква_вершины количество_ребер, например 'f 1') или 'done': ").strip().lower()
            if inp == 'done':
                break
            try:
                j_label, count = inp.split()
                count = int(count)
                if j_label not in labels:
                    print(f"Ошибка: вершина '{j_label}' не существует. Допустимые вершины: {', '.join(labels)}.")
                    continue
                j = labels.index(j_label)
                if i == j:
                    print("Ребро не может быть петлей (i == j). Используйте ввод петель для этого.")
                    continue
                if count <= 0:
                    print("Количество ребер должно быть положительным.")
                    continue
                edge = (min(i, j), max(i, j))
                edges[edge] = edges.get(edge, 0) + count
            except ValueError:
                print("Ошибка ввода. Формат: буква_вершины количество_ребер (например 'f 1').")

        print(f"\033[34m\nВвод петель для '{vertex}'. Введите '0' для пропуска или количество петель.\033[0m")
        while True:
            inp = input(f"Введите количество петель для '{vertex}' (например '1') или '0' для пропуска: ").strip()
            if inp == '0':
                break
            try:
                count = int(inp)
                if count <= 0:
                    print("Количество петель должно быть положительным.")
                    continue
                loops[i] = count
                break
            except ValueError:
                print("Ошибка ввода. Введите целое число.")

    return arcs, edges, loops

def build_s0_matrix(n, arcs, edges, loops, p_vector=None, q=1, debug=False):
    """Построение матрицы S^0 с добавлением вектора P как столбца и отладочным выводом."""
    s0 = np.zeros((n, n), dtype=int)
    labels = [chr(97 + i) for i in range(n)]

    if debug:
        print("\nВычисление матрицы S^0:")

    for i in range(n):
        for j in range(n):
            if i != j:
                e_ij = arcs.get((i, j), 0)
                o_ij = edges.get((min(i, j), max(i, j)), 0)
                s0[i, j] = e_ij * (10 ** q) + o_ij
                if debug:
                    print(f"Для ячейки [{labels[i]},{labels[j]}]: e_ij={e_ij}, o_ij={o_ij}, s0[{labels[i]},{labels[j]}] = {e_ij} * 10^{q} + {o_ij} = {s0[i,j]}")
            else:
                s0[i, j] = loops.get(i, 0)
                if debug:
                    print(f"Для ячейки [{labels[i]},{labels[j]}]: петли={s0[i,j]}")

    df = pd.DataFrame(s0, index=labels, columns=labels)

    if p_vector is not None:
        df['P'] = p_vector

    df = df.astype(str)
    df = df.replace('0', '-')

    return df

def build_sk_matrix(sk_prev, pk_prev, w=1, debug=False):
    """Построение новой матрицы S^k на основе предыдущей S^{k-1}."""
    n = sk_prev.shape[0]
    sk = np.zeros((n, n), dtype=int)
    labels = [chr(97 + i) for i in range(n)]

    if debug:
        print(f"\nВычисление матрицы S^{w}:")

    for i in range(n):
        for j in range(n):
            if sk_prev.columns[j] == 'P':
                continue  # пропускаем столбец P
            if sk_prev.iloc[i, j] != '-':
                sk_prev_value = int(sk_prev.iloc[i, j])
                sk[i, j] = sk_prev_value * (10 ** (2 * w)) + pk_prev[i] * (10 ** w) + pk_prev[j]
                if debug:
                    print(f"Для ячейки [{labels[i]},{labels[j]}]: sk_prev={sk_prev_value}, pk_prev[{labels[i]}]={pk_prev[i]}, pk_prev[{labels[j]}]={pk_prev[j]}, sk[{labels[i]},{labels[j]}]={sk[i,j]}")

    df = pd.DataFrame(sk, index=labels, columns=labels)
    df['P'] = pk_prev
    df = df.astype(str)
    df = df.replace('0', '-')
    return df

def get_lh_sets(matrix):
    """Получение наборов локальных характеристик (ЛХ) для строк матрицы."""
    lh_sets = []
    for _, row in matrix.iloc[:, :-1].iterrows():
        non_zero = sorted([int(x) for x in row if x != '-'])
        lh_sets.append(tuple(non_zero))
    return lh_sets

def assign_codes(lh_sets):
    """Присвоение кодов уникальным наборам ЛХ."""
    unique_lh = set(lh_sets)
    code_map = {lh: idx + 1 for idx, lh in enumerate(unique_lh)}
    return [code_map[lh] for lh in lh_sets]

def format_dataframe(df):
    """Форматирование DataFrame для вывода с одинаковой шириной столбцов."""
    col_widths = {}
    for col in df.columns:
        max_len = max(len(str(col)), df[col].astype(str).map(len).max())
        col_widths[col] = max_len + 2
    return col_widths

def print_colored_dataframe(df, col_widths):
    """Вывод DataFrame с цветным столбцом P и правильным выравниванием."""
    header = '   '
    for col in df.columns:
        header += f"{col:>{col_widths[col]}} "
    print(header)

    for idx, row in df.iterrows():
        line = f"{idx:<2} "
        for col in df.columns[:-1]:
            line += f"{row[col]:>{col_widths[col]}} "
        line += f"\033[95m{row['P']:>{col_widths['P']}}\033[0m"
        print(line)

def print_graph_info(n, arcs, edges, loops, graph_name):
    """Вывод информации о дугах, ребрах и петлях графа."""
    labels = [chr(97 + i) for i in range(n)]
    print(f"\nИнформация о графе {graph_name}:")

    print("Дуги:")
    if arcs:
        for (i, j), count in sorted(arcs.items(), key=lambda x: (x[0][0], x[0][1])):
            print(f"{labels[i]} -> {labels[j]}: {count}")
    else:
        print("Нет дуг")

    print("Ребра:")
    if edges:
        for (u, v), count in sorted(edges.items(), key=lambda x: (x[0][0], x[0][1])):
            print(f"{{{labels[u]}, {labels[v]}}}: {count}")
    else:
        print("Нет ребер")

    print("Петли:")
    if loops:
        for i, count in sorted(loops.items()):
            print(f"{labels[i]}: {count}")
    else:
        print("Нет петель")

def are_graphs_isomorphic(g_arcs, g_edges, g_loops, h_arcs, h_edges, h_loops, n, debug=False):
    """Проверка изоморфизма двух графов с новым форматированием и отладочным выводом."""
    if not (g_arcs or g_edges or g_loops):
        print("Ошибка: Граф G пуст (нет дуг, ребер или петель).")
        return False, None
    if not (h_arcs or h_edges or h_loops):
        print("Ошибка: Граф H пуст (нет дуг, ребер или петель).")
        return False, None

    p0_g = [0] * n
    p0_h = [0] * n
    s0_g = build_s0_matrix(n, g_arcs, g_edges, g_loops, p0_g, debug=debug)
    s0_h = build_s0_matrix(n, h_arcs, h_edges, h_loops, p0_h, debug=debug)

    lh_g = get_lh_sets(s0_g)
    lh_h = get_lh_sets(s0_h)

    if not lh_g or not lh_h:
        print("Ошибка: Один из графов не содержит ненулевых локальных характеристик (все элементы матрицы S^0 равны '-').")
        return False, None

    if set(lh_g) != set(lh_h):
        print("Локальные характеристики на шаге 0 не совпадают.")
        return False, None

    p0_g = assign_codes(lh_g)
    p0_h = assign_codes(lh_h)

    s0_g = build_s0_matrix(n, g_arcs, g_edges, g_loops, p0_g, debug=debug)
    s0_h = build_s0_matrix(n, h_arcs, h_edges, h_loops, p0_h, debug=debug)

    col_widths_g = format_dataframe(s0_g)
    col_widths_h = format_dataframe(s0_h)
    print("\nМатрица S^0(G):")
    print_colored_dataframe(s0_g, col_widths_g)
    print("\nМатрица S^0(H):")
    print_colored_dataframe(s0_h, col_widths_h)

    pk_g, pk_h = p0_g, p0_h
    sk_g, sk_h = s0_g, s0_h
    iteration = 0

    while True:
        print(f"\nОтладка (итерация {iteration}): pk_g = {pk_g}, pk_h = {pk_h}")
        unique_codes_g = len(set(pk_g))
        unique_codes_h = len(set(pk_h))
        print(f"Уникальных кодов: G = {unique_codes_g}, H = {unique_codes_h}")

        if unique_codes_g == n and unique_codes_h == n:
            if set(pk_g) == set(pk_h):
                mapping = {}
                g_codes = sorted([(code, i) for i, code in enumerate(pk_g)])
                h_codes = sorted([(code, i) for i, code in enumerate(pk_h)])
                for (g_code, g_idx), (h_code, h_idx) in zip(g_codes, h_codes):
                    if g_code != h_code:
                        print("Коды не совпадают при полной дифференциации.")
                        return False, None
                    mapping[chr(97 + g_idx)] = chr(97 + h_idx)
                print(f"Отладка: mapping = {mapping}")
                return True, mapping
            else:
                print("Наборы кодов не совпадают при полной дифференциации.")
                return False, None

        if not pk_g or not pk_h:
            print("Ошибка: Векторы P^k пусты. Вероятно, графы не содержат связей.")
            return False, None

        if iteration >= n:
            print(f"Достигнуто максимальное количество итераций ({n}). Графы не изоморфны.")
            return False, None

        if max(pk_g) > n or max(pk_h) > n:
            print("Максимальный код превышает количество вершин. Графы не изоморфны.")
            return False, None

        sk_g = build_sk_matrix(s0_g, pk_g, w=1, debug=debug)
        sk_h = build_sk_matrix(s0_h, pk_h, w=1, debug=debug)

        lh_g = get_lh_sets(sk_g)
        lh_h = get_lh_sets(sk_h)

        if not lh_g or not lh_h:
            print(f"Ошибка на итерации {iteration + 1}: Один из графов не содержит ненулевых локальных характеристик.")
            return False, None

        if set(lh_g) != set(lh_h):
            print(f"Локальные характеристики на итерации {iteration + 1} не совпадают.")
            return False, None

        pk_g = assign_codes(lh_g)
        pk_h = assign_codes(lh_h)

        iteration += 1
        col_widths_g = format_dataframe(sk_g)
        col_widths_h = format_dataframe(sk_h)
        print(f"\nИтерация {iteration}:")
        print(f"Матрица S^{iteration}(G):")
        print_colored_dataframe(sk_g, col_widths_g)
        print(f"\nМатрица S^{iteration}(H):")
        print_colored_dataframe(sk_h, col_widths_h)

def main():
    while True:
        mode = input("Выберите режим (1 - обычный, 2 - отладочный): ").strip()
        if mode in ['1', '2']:
            break
        print("Неверный выбор. Введите 1 или 2.")

    debug = mode == '2'

    if mode == '2':
        n = 8
        print(f"\nОтладочный режим: n = {n}")
        if not os.path.exists("t_graph_g.txt"):
            print("Ошибка: Файл t_graph_g.txt не найден. Пожалуйста, предоставьте файл и запустите программу снова.")
            return
        if not os.path.exists("t_graph_h.txt"):
            print("Ошибка: Файл t_graph_h.txt не найден. Пожалуйста, предоставьте файл и запустите программу снова.")
            return
        print("\nЗагружаю граф G из t_graph_g.txt...")
        g_arcs, g_edges, g_loops = read_graph_from_file(n, "t_graph_g.txt")
        if g_arcs is None:
            return
        print("\nЗагружаю граф H из t_graph_h.txt...")
        h_arcs, h_edges, h_loops = read_graph_from_file(n, "t_graph_h.txt")
        if h_arcs is None:
            return

        print_graph_info(n, g_arcs, g_edges, g_loops, "G")
        print_graph_info(n, h_arcs, h_edges, h_loops, "H")
    else:
        while True:
            try:
                n = int(input("Введите количество вершин графа (n): "))
                if n > 0:
                    break
                else:
                    print("Количество вершин должно быть положительным.")
            except ValueError:
                print("Введите целое число.")

        while True:
            choice_g = input("\nКак вводить граф G? (1 - вручную, 2 - из файла): ").strip()
            if choice_g == '1':
                print("\nВвод графа G вручную:")
                g_arcs, g_edges, g_loops = input_graph(n)
                print(f"Сохраняю граф G в файл graph_input_g.txt...")
                save_graph_to_file(n, g_arcs, g_edges, g_loops, "graph_input_g.txt")
                break
            elif choice_g == '2':
                print("\nВвод графа G из файла (graph_input_g.txt):")
                g_arcs, g_edges, g_loops = read_graph_from_file(n, "graph_input_g.txt")
                if g_arcs is None:
                    return
                break
            else:
                print("Неверный выбор. Введите 1 или 2.")

        while True:
            choice_h = input("\nКак вводить граф H? (1 - вручную, 2 - из файла): ").strip()
            if choice_h == '1':
                print("\nВвод графа H вручную:")
                h_arcs, h_edges, h_loops = input_graph(n)
                print("Сохраняю граф H в файл graph_input_h.txt...")
                save_graph_to_file(n, h_arcs, h_edges, h_loops, "graph_input_h.txt")
                break
            elif choice_h == '2':
                print("\nВвод графа H из файла (graph_input_h.txt):")
                h_arcs, h_edges, h_loops = read_graph_from_file(n, "graph_input_h.txt")
                if h_arcs is None:
                    return
                break
            else:
                print("Неверный выбор. Введите 1 или 2.")

    is_isomorphic, mapping = are_graphs_isomorphic(g_arcs, g_edges, g_loops, h_arcs, h_edges, h_loops, n, debug=debug)

    if is_isomorphic:
        print("\nГрафы изоморфны.")
        if mapping is not None:
            print("Соответствие вершин (G -> H):")
            for x, y in sorted(mapping.items()):
                print(f"{x} -> {y}")
        else:
            print("Ошибка: Соответствие вершин не определено, хотя графы изоморфны.")
    else:
        print("\nГрафы не изоморфны.")

if __name__ == "__main__":
    main()
