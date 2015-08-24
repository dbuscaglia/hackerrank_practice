class REGraph(object):

    def __init__(self):
        self.rs_agents = []

    def init_graph(self, size, **kwargs):
        #  Tradeoffs here - List takes less memory if graph is sparse
        #   but has slower lookup.
        def init_matrix(size):
            """
            Initializes an adjacency matrix with a given NxN
            """
            matrix = []
            for y in xrange(size):
                matrix[y] = []
                for x in xrange(size):
                    matrix[y][x] = False

            return matrix

        def init_list(size):
            return {}

        if kwargs.get("use_list", False):
            self.graph = init_list(size)
            self.graph_type = "list"
        else:
            self.graph = init_matrix(size)
            self.graph_type = "matrix"
        self.total_rs_agents = 0
        self.total_regular_agents = 0

    def set_vertex(self, agent):
        if self.graph_type == "list":
            self.graph[agent.agent_id] = set()
        return True

    def in_graph(self, aid):
        try:
            return self.graph[aid]
        except KeyError:
            return False

    def ensure_add_agent(self, agent):
        if not self.in_graph(agent.agent_id):
            self.set_vertex(agent)
            if agent.rs_agent:
                self.rs_agents.append(agent.agent_id)
                self.total_rs_agents = self.total_rs_agents + 1
            else:
                self.total_regular_agents = self.total_regular_agents + 1

    def connect(self, agent1, agent2):
        self.connect_vertices(agent1, agent2)

    def connect_vertices(self, agent1, agent2):
        self.ensure_add_agent(agent1)
        self.graph[agent1.agent_id].add(agent2)
        self.ensure_add_agent(agent2)
        self.graph[agent2.agent_id].add(agent1)

    def bfs(self, start_agent, max_depth=2):
        eligable = set()
        u = Agent(start_agent, is_rs_agent=True)
        u.visit(None)
        u.visited = True
        q = [u]
        while q:
            v = q.pop(0)
            if v.depth <= max_depth:
                for neighbor in self.graph[v.agent_id]:
                    if not neighbor.visited and neighbor.agent_id != u.agent_id:
                        neighbor.visit(v)
                        q.append(neighbor)
                        if v.depth == max_depth:
                            # Only interested in max_depth
                            if neighbor.agent_id not in eligable:
                                # only count second degree connections
                                eligable.add(neighbor.agent_id)

        return eligable


class Agent(object):

    def __init__(self, agent_id, is_rs_agent=False):
        self.agent_id = agent_id
        self.rs_agent = is_rs_agent
        self.visited = False
        self.connected = False

    def visit(self, origin):
        self.visited = True
        self.parent = origin
        if not origin:
            self.depth = 1
        else:
            self.depth = origin.depth + 1


transaction_count = int(raw_input())
current_transaction = 0

re_graph = REGraph()
kwargs = {"use_list": True}
re_graph.init_graph(transaction_count, **kwargs)

while current_transaction < transaction_count:
    transaction = raw_input()
    # capture transaction
    output = transaction.split(",")
    agent1_id = output[0]
    try:
        agent1_is_rs_agent = any(output[1])
    except ValueError, IndexError:
        agent1_is_rs_agent = False
    agent2_id = output[2]
    try:
        agent2_is_rs_agent = any(output[3])
    except ValueError, IndexError:
        agent2_is_rs_agent = False

    agent1 = Agent(agent1_id.lower(), agent1_is_rs_agent)
    agent2 = Agent(agent2_id.lower(), agent2_is_rs_agent)
    if (agent1.agent_id != agent2.agent_id and (agent1.agent_id != "" or not agent1.agent_id or agent1.agent_id == "None")
        and agent2.agent_id != "" or not agent2.agent_id or agent2.agent_id == "None"):
        re_graph.connect(agent1, agent2)

    current_transaction += 1

final_set = set()
for rs_agent in re_graph.rs_agents:
    agents = re_graph.bfs(rs_agent)
    if agents:
        final_set = set.union(final_set, agents)

percentage = float(len(final_set)) / (re_graph.total_rs_agents + re_graph.total_regular_agents)
print "{0:.5f}".format(percentage)
