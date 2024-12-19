import sys  # Модуль для работы с системными параметрами. Используется для получения максимального значения для обозначения "бесконечности" (sys.maxsize) в матрице смежности.
import networkx as nx  # Библиотека для работы с графами. Используется для создания графа, выполнения алгоритмов на графах (например, поиска кратчайшего пути) и визуализации графа.
import matplotlib.pyplot as plt  # Библиотека для создания визуализаций. Используется для отрисовки графа и его рёбер на экране.
from collections import defaultdict, deque  # Модуль для работы с специализированными типами данных. defaultdict упрощает создание списка для каждой вершины, deque используется для построения пути в алгоритме Дейкстры.

class Graph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        # defaultdict(list) используется, чтобы автоматически создавать пустые списки для новых вершин
        # Удобно для представления графа, так как можно сразу добавлять рёбра без проверки существования ключа.
        self.adjacency_list = defaultdict(list)
        # Используем set для хранения всех вершин, так как set автоматически управляет уникальностью элементов.
        self.vertices = set()

    def add_edge(self, src, dest, weight):
        # Добавление ребра в граф, с учётом направления (src -> dest).
        # Вершины src и dest добавляются в множество вершин.
        self.adjacency_list[src].append((dest, weight))
        self.vertices.add(src)
        self.vertices.add(dest)

    def remove_vertex(self, vertex):
        # Удаление вершины из графа. Также нужно удалить все рёбра, связанные с этой вершиной.
        if vertex in self.vertices:
            self.vertices.remove(vertex)
            self.adjacency_list.pop(vertex, None)
            for src in self.adjacency_list:
                self.adjacency_list[src] = [(dest, weight) for dest, weight in self.adjacency_list[src] if dest != vertex]

    def add_vertex(self, vertex):
        # Добавление новой вершины в множество вершин, если её ещё нет.
        if vertex not in self.vertices:
            self.vertices.add(vertex)

    def create_adjacency_matrix(self):
        # Создание матрицы смежности для графа, используя индексированные вершины.
        # sys.maxsize используется для обозначения "бесконечности", чтобы обозначить отсутствие рёбер.
        matrix = [[sys.maxsize] * len(self.vertices) for _ in range(len(self.vertices))]
        vertex_to_index = {vertex: idx for idx, vertex in enumerate(sorted(self.vertices))}

        for src in self.adjacency_list:
            for dest, weight in self.adjacency_list[src]:
                matrix[vertex_to_index[src]][vertex_to_index[dest]] = weight
                matrix[vertex_to_index[dest]][vertex_to_index[src]] = weight

        return matrix, vertex_to_index
    
    def print_adjacency_matrix(self, matrix, vertices):
        # Печать матрицы смежности. Вершины отображаются с их индексами.
        print("\nAdjacency Matrix:")
        col_width = 6  
        header = " " * col_width + "".join(f"{v:>{col_width}}" for v in vertices)
        print(header)

        for i, row in enumerate(matrix):
            row_str = f"{vertices[i]:>{col_width}}"
            for val in row:
                if val == sys.maxsize:
                    row_str += f"{'INF':>{col_width}}"
                else:
                    row_str += f"{val:>{col_width}}"
            print(row_str)
        
    def dijkstra(self, start, end):
        # Алгоритм Дейкстры для поиска кратчайшего пути между вершинами.
        # unvisited - словарь, где хранятся минимальные расстояния от стартовой вершины до каждой вершины.
        # processed - множество для отслеживания посещённых вершин.
        # predecessors - словарь для восстановления пути от конечной вершины к начальной.
        unvisited = {vertex: sys.maxsize for vertex in self.vertices}
        unvisited[start] = 0
        visited = {}
        processed = set()
        predecessors = {}

        print("\nInitial state:")
        print(f"Unvisited: {unvisited}")
        print(f"Processed: {processed}")

        while unvisited:
            # Выбираем вершину с минимальным расстоянием
            current_vertex = min(unvisited, key=unvisited.get)
            current_distance = unvisited[current_vertex]

            print(f"\nVisiting vertex: {current_vertex}, Distance: {current_distance}")

            if current_vertex not in processed:
                processed.add(current_vertex)

            for neighbor, weight in self.adjacency_list[current_vertex]:
                if neighbor not in visited:
                    new_distance = current_distance + weight
                    if new_distance < unvisited[neighbor]:
                        unvisited[neighbor] = new_distance
                        predecessors[neighbor] = current_vertex
                    print(f"Updated: {neighbor}, Distance: {new_distance}")

            visited[current_vertex] = current_distance
            unvisited.pop(current_vertex)
            print(f"Processed: {processed}")
            print(f"Unvisited: {unvisited}")

            if current_vertex == end:
                break

        # Восстановление пути из конечной вершины в начальную.
        path = deque()
        current = end
        while current in predecessors:
            path.appendleft(current)
            current = predecessors[current]
        if path:
            path.appendleft(start)

        return list(path), visited.get(end, sys.maxsize)

    def visualize(self):
        # Визуализация графа с помощью NetworkX и matplotlib.
        # G - граф, представленный как объект NetworkX DiGraph.
        # Используется для отображения графа и рёбер с весами.
        G = nx.DiGraph()
        for src in self.adjacency_list:
            for dest, weight in self.adjacency_list[src]:
                G.add_edge(src, dest, weight=weight)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=12, font_weight="bold")
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.title("Graph Visualization")
        plt.show()


def main():
    # Запрос числа вершин у пользователя
    num_vertices = int(input("Enter the number of vertices: "))
    graph = Graph(num_vertices)  # Создание объекта графа с заданным количеством вершин

    # Ввод вершин и рёбер
    print("Enter the vertices in the format: Vertex Distance PreviousVertex (use 0 for distance to the starting vertex):")
    for _ in range(num_vertices):
        data = input().split()  # Ввод данных о вершине
        vertex = data[0]  # Имя вершины
        distance = int(data[1])  # Расстояние до вершины
        if len(data) > 2:
            previous_vertex = data[2]  # Предыдущая вершина для рёбер
            graph.add_edge(previous_vertex, vertex, distance)  # Добавление рёбер в граф
        else:
            graph.add_edge(vertex, vertex, 0)  # Если нет предыдущей вершины, то добавляем само-себе с весом 0

    # Главный цикл программы
    while True:
        matrix, vertex_to_index = graph.create_adjacency_matrix()  # Генерация матрицы смежности
        vertices_sorted = sorted(graph.vertices)  # Сортировка вершин
        graph.print_adjacency_matrix(matrix, vertices_sorted)  # Печать матрицы смежности

        # Запрос на ввод начальной и конечной вершины для поиска кратчайшего пути
        start, end = input("Enter the start and end vertices separated by a space: ").split()
        path, distance = graph.dijkstra(start, end)  # Поиск кратчайшего пути
        if distance == sys.maxsize:
            print(f"No path exists between {start} and {end}.")  # Если путь не найден
        else:
            print(f"Shortest path from {start} to {end}: {' -> '.join(path)}")
            print(f"Total distance: {distance}")  # Вывод кратчайшего пути и его длины

        # Цикл для выполнения дополнительных действий
        while True:
            # Запрос действия от пользователя
            action = input("\nChoose an action: [add, del, next, quit, visualize]: ").strip().lower()
            if action == "add":
                vertex = input("Enter the name of the vertex to add: ").strip()  # Ввод новой вершины
                graph.add_vertex(vertex)  # Добавление вершины в граф
                print(f"Vertex '{vertex}' added.")
            elif action == "del":
                vertex = input("Enter the name of the vertex to remove: ").strip()  # Ввод вершины для удаления
                graph.remove_vertex(vertex)  # Удаление вершины из графа
                print(f"Vertex '{vertex}' removed.")
            elif action == "next":
                break  # Переход к следующему циклу
            elif action == "quit":
                print("Exiting program.")  # Завершение работы программы
                return
            elif action == "visualize":
                graph.visualize()  # Визуализация графа
            else:
                print("Invalid action. Please try again.")  # Если введено неверное действие
