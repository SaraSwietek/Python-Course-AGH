class Graph():
    def __init__(self):
        self.graph = {}

    def show_graph(self):
        print(self.graph)

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = set()

    def remove_vertex(self, vertex):
        # usuwam klucz
        self.graph.pop(vertex, None)

        # usuwanie wszystkich przyleglych krawedzi (jesli istnieja)
        for i in self.graph.values():
            if vertex in i:
                i.remove(vertex)

    def add_edge(self, v_start, v_end):
        if v_start not in self.graph:
            self.graph[v_start] = {v_end}
            if v_end not in self.graph:
                self.graph[v_end] = {v_start}
            else:
                self.graph[v_end].add(v_start)
        else:
            self.graph[v_start].add(v_end)
            if v_end not in self.graph:
                self.graph[v_end] = {v_start}
            else:
                self.graph[v_end].add(v_start)

    def remove_edge(self, v_start, v_end):
        if (v_start in self.graph.keys()) and (v_end in self.graph.keys()):
            if v_start in self.graph[v_end]:
                self.graph[v_end].remove(v_start)
            if v_end in self.graph[v_start]:
                self.graph[v_start].remove(v_end)

    def get_neighbours(self, vertex):
        return self.graph[vertex]

    def DFS(self, vertex, visited = [], stack = []):

        if vertex not in visited:
            visited.append(vertex)

        for i in self.get_neighbours(vertex):
            if i not in visited:
                stack.append(i)

        vertex = stack[-1]
        stack = stack[:-1]

        #print("vertex: ", vertex)
        #print("visited: ", visited)
        #print("stack: ", stack)

        if len(stack)>0:
            return self.DFS(vertex, visited, stack)
        else:
            if vertex not in visited: #zabezpieczenie: jesli vertex nie jest w visited a stack jest juz pusty
                visited.append(vertex)
            return iter(visited)

    def BFS(self, vertex, visited = [], queue = []):

        if vertex not in visited:
            visited.append(vertex)

        for i in self.get_neighbours(vertex):
            if i not in visited:
                queue.append(i)
                visited.append(i) #od razu dodaje wierzcholki do odwiedzonych

        vertex = queue[0]
        queue = queue[1:]

        #print("vertex: ", vertex)
        #print("visited: ", visited)
        #print("queue: ", queue)

        if len(queue)>0:
            return self.BFS(vertex, visited, queue)
        else:
            if vertex not in visited:
                visited.append(vertex)
            return iter(visited)

if __name__ == '__main__':
    graph = Graph()

    #graf przykladowy:
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(0, 3)
    graph.add_edge(1, 3)
    graph.add_edge(2, 3)
    graph.add_edge(3, 5)
    graph.add_edge(4, 2)
    graph.add_edge(4, 6)

    graph.show_graph()

    root = 0 #przegladamy od wierzcholka 0

    try:
        print("DFS: ")
        for vertex in graph.DFS(root):
            print(vertex)

    except KeyError:
        print("Nie znaleziono podanego korzenia w grafie")
    except IndexError:
        print("Korzen nie posiada krawedzi")

    try:
        print("BFS: ")
        for vertex in graph.BFS(root):
            print(vertex)

    except KeyError:
        print("Nie znaleziono podanego korzenia w grafie")
    except IndexError:
        print("Korzen nie posiada krawedzi")


