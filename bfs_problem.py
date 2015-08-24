def two_int_inputs():
    return map(int, raw_input().split(' '))

number_test_cases = int(raw_input())
total_nodes, total_edges = two_int_inputs()


class vertex(object):

    def __init__(self, name):
        self.name = name
        self.visited = False
        self.neighbors = set()
        self.output = []
        self.depth = 0
        self.weight = -1

    def visit(self, parent, weight):
        self.visited = True
        self.parent = parent
        try:
            self.depth = parent.depth + 1
            self.weight = parent.weight + weight
        except AttributeError:
            # Origin
            self.depth = 0
            self.weight = 0
        self.visit_work()

    def connect(self, neighbor_name, weight):
        self.neighbors.add((neighbor_name, weight))

    def visit_work(self):
        pass


class list_graph(object):
    data = {}
    node_names = set()

    def ensure_node(self, node_value):
        self.node_names.add(node_value)
        exists = self.data.get(node_value, None)
        if not exists:
            node = vertex(node_value)
            self.data[node_value] = node

    def connect(self, first_node, second_node, weight=0):
        graph.ensure_node(first_node)
        graph.ensure_node(second_node)
        self.data[first_node].connect(second_node, weight)
        self.data[second_node].connect(first_node, weight)

    def bft(self, start_node):
        u = self.data.get(start_node)
        u.visit(None, 0)
        u.visited = True
        q = [u]
        while q:
            v = q.pop(0)
            for neighbor_name, weight in v.neighbors:
                neighbor = self.data.get(neighbor_name)
                if not neighbor.visited:
                    neighbor.visit(v, weight)
                    q.append(neighbor)
        return True

    def print_visits(self, start_position):
        output = []
        for node in self.node_names:
            if node != start_position:
                if not self.data.get(node).visited:
                    output.append(-1)
                else:
                    v = self.data.get(node)
                    output.append(v.weight)
        print ' '.join(map(str, output))

graph = list_graph()

for testcase in xrange(total_edges):
    first_node, second_node = two_int_inputs()
    graph.connect(first_node, second_node, 6)

missing_nodes = len(graph.node_names) < total_nodes
if missing_nodes:
    missing_start = max(graph.node_names)
    for i in xrange(missing_start + 1, missing_nodes + missing_start + 1, 1):
        graph.ensure_node(i)


start_position = int(raw_input())
graph.bft(start_position)
graph.print_visits(start_position)
