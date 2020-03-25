from graphviz import Digraph


class Concept:
    def __init__(self, name):
        self.name = name
        self.children = []

    def get_name(self):
        return self.name

    def link_child(self, other_concept):
        self.children.append(other_concept)

    def nodes(self, dot, depth):
        if depth == 0:
            return

        dot.node(self.name, self.name)
        for child in self.children:
            child.nodes(dot, depth - 1)

    def edges(self, dot, depth):
        if depth == 0:
            return

        for child in self.children:
            dot.edge(self.name, child.get_name())
            child.edges(dot, depth - 1)

    def graph(self, dot, depth):
        self.nodes(dot, depth)
        self.edges(dot, depth)

    def render_dot_graph(self, output, depth = 10000):
        dot = Digraph(graph_attr={'rankdir': 'LR'})
        self.graph(dot, depth)
        dot.render(output, view=True, format='png')

    def find(self, name):
        if self.name == name:
            return self
        else:
            for child in self.children:
                rez = child.find(name)
                if rez is not None:
                    return rez
