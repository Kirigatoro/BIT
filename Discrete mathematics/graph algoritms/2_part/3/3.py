from prettytable import PrettyTable
from termcolor import colored


def parse_graph(file_path):
	vertices = {}
	try:
		with open(file_path, 'r') as file:
			current_vertex = None
			for line in file:
				line = line.strip()
				if not line:
					continue
				if line.isalpha() and len(line) == 1:
					current_vertex = line
					vertices[current_vertex] = {'arcs': {}, 'edges': {}, 'loops': 0}
				elif current_vertex and ':' in line:
					key, value = line.split(':', 1)
					key = key.strip()
					value = value.strip()
					if key == 'loops':
						vertices[current_vertex]['loops'] = int(value)
					else:
						if value == '0':
							continue
						pairs = value.split(';')
						for pair in pairs:
							vertex, weight = pair.strip().split()
							vertices[current_vertex][key][vertex] = int(weight)
		return vertices
	except FileNotFoundError:
		print(f"Файл {file_path} не найден.")
		return {}
	except Exception as e:
		print(f"Ошибка при парсинге файла: {e}")
		return {}


def print_matrix(matrix, name, colon_name, row_name, highlight_column=None, max_width=4):
	if not matrix or not matrix[0]:
		print("Матрица пуста")
		return
	table = PrettyTable()
	num_columns = len(matrix[0])
	table.field_names = [name] + colon_name[:num_columns]
	table.vertical_char = ' '
	table.junction_char = ' '
	for i, row in enumerate(matrix):
		row_label = row_name[i]
		formatted_row = ['-' if val == 0 else str(val) for val in row]
		if highlight_column is not None:
			formatted_row[highlight_column] = colored(formatted_row[highlight_column], 'cyan')
		table.add_row([row_label] + formatted_row)
	for field in table.field_names:
		table._max_width[field] = max_width  # Фиксированная ширина 3 символа
		table.align[field] = "c"  # Центральное выравнивание
	table.border = False
	print()
	print(table)
	print()


def build_s_0(vertices, vertex_list):
	n = len(vertex_list)
	s0 = [[0] * n for _ in range(n)]
	for i, vertex in enumerate(vertex_list):
		s0[i][i] = vertices[vertex]['loops']
		args = [j for j in vertices[vertex]['arcs']]
		edges = [j for j in vertices[vertex]['edges']]
		for j in range(n):
			k = vertex_list[j]
			if k in args:
				s0[i][j] += vertices[vertex]['arcs'][k] * 10
			if k in edges:
				s0[i][j] += vertices[vertex]['edges'][k]
	return s0


def build_p(matrix_g, matrix_h):
	row_to_index = {}
	current_index = 1
	p_g = []
	p_h = []
	for row in matrix_g:
		sorted_row = tuple(sorted(row))
		if sorted_row in row_to_index:
			p_g.append(row_to_index[sorted_row])
		else:
			row_to_index[sorted_row] = current_index
			p_g.append(current_index)
			current_index += 1
	for row in matrix_h:
		sorted_row = tuple(sorted(row))
		if sorted_row in row_to_index:
			p_h.append(row_to_index[sorted_row])
		else:
			print("Ошибка Графы не изоморфны")
			exit(1)
	return p_g, p_h


def build_s_k(s0, p, vertex_list):
	n = len(vertex_list)
	sk = [[0] * n for _ in range(n)]
	for i in range(n):
		for j in range(n):
			if s0[i][j] != 0:
				sk[i][j] = s0[i][j] * 100 + p[i] * 10 + p[j]
	return sk


def main():
	graph_g = "graph_g.txt"
	graph_h = "graph_h.txt"
	pg = [0]
	ph = [0]

	vertices_g = parse_graph(graph_g)
	vertices_h = parse_graph(graph_h)

	vertex_list_g = sorted(vertices_g.keys())
	vertex_list_h = sorted(vertices_h.keys())

	s0_g = build_s_0(vertices_g, vertex_list_g)
	s0_h = build_s_0(vertices_h, vertex_list_h)
	print('\n\n\n')
	print_matrix(s0_g, 'G_0', vertex_list_g, vertex_list_g)
	print_matrix(s0_h, 'H_0', vertex_list_h, vertex_list_h)
	pg[0], ph[0] = build_p(s0_g, s0_h)
	print('G>>>>>>', pg)
	print('H>>>>>>', ph)

	flag = True
	iteration = 1
	end = [i for i in range(1, len(vertex_list_g) + 1)]

	while flag:
		pg.append(0)
		ph.append(0)
		sg = build_s_k(s0_g, pg[iteration - 1], vertex_list_g)
		sh = build_s_k(s0_h, ph[iteration - 1], vertex_list_h)
		pg[iteration], ph[iteration] = build_p(sg, sh)
		name_g = 'G_' + str(iteration)
		name_h = 'H_' + str(iteration)

		print_matrix(sg, name_g, vertex_list_g, vertex_list_g)
		print_matrix(sh, name_h, vertex_list_h, vertex_list_h)

		print_matrix(pg, "P_G", vertex_list_g, range(len(vertex_list_g)))
		print_matrix(ph, "P_H", vertex_list_h, range(len(vertex_list_h)))

		print('>>>>>>>>>', pg[iteration], '>>>', sorted(ph[iteration]), '>>', end)
		if pg[iteration] == sorted(ph[iteration]) == end:
			break
		iteration += 1

	answer_g = vertex_list_g
	answer_h = [0] * len(vertex_list_h)
	counter = 0
	for i in ph[iteration]:
		answer_h[i - 1] = vertex_list_h[counter]
		counter += 1
	print('\n\n Ответ')
	print('G -> ', answer_g)
	print('H -> ', answer_h)


if __name__ == "__main__":
	main()
