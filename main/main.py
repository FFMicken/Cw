import sys
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict, deque

class Graph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.adjacency_list = defaultdict(list)
        self.vertices = set()

    def add_edge(self, src, dest, weight):
        self.adjacency_list[src].append((dest, weight))
        self.vertices.add(src)
        self.vertices.add(dest)

    def remove_vertex(self, vertex):
        if vertex in self.vertices:
            self.vertices.remove(vertex)
            self.adjacency_list.pop(vertex, None)
            for src in self.adjacency_list:
                self.adjacency_list[src] = [(dest, weight) for dest, weight in self.adjacency_list[src] if dest != vertex]

    def add_vertex(self, vertex):
        if vertex not in self.vertices:
            self.vertices.add(vertex)

    def create_adjacency_matrix(self):
        matrix = [[sys.maxsize] * len(self.vertices) for _ in range(len(self.vertices))]
        vertex_to_index = {vertex: idx for idx, vertex in enumerate(sorted(self.vertices))}

        # Обновляем матрицу для двусторонних рёбер
        for src in self.adjacency_list:
            for dest, weight in self.adjacency_list[src]:
                matrix[vertex_to_index[src]][vertex_to_index[dest]] = weight
                matrix[vertex_to_index[dest]][vertex_to_index[src]] = weight  # Обновляем для обратного пути

        return matrix, vertex_to_index
    
    def print_adjacency_matrix(self, matrix, vertices):
        print("\nAdjacency Matrix:")
        # Ширина столбца
        col_width = 6  
        # Заголовки столбцов
        header = " " * col_width + "".join(f"{v:>{col_width}}" for v in vertices)
        print(header)

        # Печать каждой строки
        for i, row in enumerate(matrix):
            row_str = f"{vertices[i]:>{col_width}}"  # Начало строки с названием вершины
            for val in row:
                if val == sys.maxsize:
                    row_str += f"{'INF':>{col_width}}"
                else:
                    row_str += f"{val:>{col_width}}"
            print(row_str)
        
    def dijkstra(self, start, end):
        unvisited = {vertex: sys.maxsize for vertex in self.vertices}
        unvisited[start] = 0
        visited = {}
        processed = set()
        predecessors = {}

        print("\nInitial state:")
        print(f"Unvisited: {unvisited}")
        print(f"Processed: {processed}")

        while unvisited:
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

        path = deque()
        current = end
        while current in predecessors:
            path.appendleft(current)
            current = predecessors[current]
        if path:
            path.appendleft(start)

        return list(path), visited.get(end, sys.maxsize)

    def visualize(self):
        # Create a graph using networkx
        G = nx.DiGraph()
        for src in self.adjacency_list:
            for dest, weight in self.adjacency_list[src]:
                G.add_edge(src, dest, weight=weight)

        # Draw the graph
        pos = nx.spring_layout(G)  # Positioning for the nodes
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=12, font_weight="bold")
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.title("Graph Visualization")
        plt.show()


def main():
    num_vertices = int(input("Enter the number of vertices: "))
    graph = Graph(num_vertices)

    print("Enter the vertices in the format: Vertex Distance PreviousVertex (use 0 for distance to the starting vertex):")
    for _ in range(num_vertices):
        data = input().split()
        vertex = data[0]
        distance = int(data[1])
        if len(data) > 2:
            previous_vertex = data[2]
            graph.add_edge(previous_vertex, vertex, distance)
        else:
            graph.add_edge(vertex, vertex, 0)

    while True:
        matrix, vertex_to_index = graph.create_adjacency_matrix()
        vertices_sorted = sorted(graph.vertices)
        graph.print_adjacency_matrix(matrix, vertices_sorted)

        start, end = input("Enter the start and end vertices separated by a space: ").split()
        path, distance = graph.dijkstra(start, end)
        if distance == sys.maxsize:
            print(f"No path exists between {start} and {end}.")
        else:
            print(f"Shortest path from {start} to {end}: {' -> '.join(path)}")
            print(f"Total distance: {distance}")

        while True:
            action = input("\nChoose an action: [add, del, next, quit, visualize]: ").strip().lower()
            if action == "add":
                vertex = input("Enter the name of the vertex to add: ").strip()
                graph.add_vertex(vertex)
                print(f"Vertex '{vertex}' added.")
            elif action == "del":
                vertex = input("Enter the name of the vertex to remove: ").strip()
                graph.remove_vertex(vertex)
                print(f"Vertex '{vertex}' removed.")
            elif action == "next":
                break
            elif action == "quit":
                print("Exiting program.")
                return
            elif action == "visualize":
                graph.visualize()
            else:
                print("Invalid action. Please try again.")

if __name__ == "__main__":
    main()
