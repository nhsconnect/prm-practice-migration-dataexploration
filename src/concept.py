from graphviz import Digraph


class Concept:
    def __init__(self, name):
        self.name = name
        self.children = []

    def get_name(self):
        return self.name

    def link_child(self, other_concept):
        self.children.append(other_concept)

    def nodes(self, dot):
        dot.node(self.name, self.name)
        for child in self.children:
            child.nodes(dot)

    def edges(self, dot):
        for child in self.children:
            dot.edge(self.name, child.get_name())
            child.edges(dot)

    def graph(self, dot):
        self.nodes(dot)
        self.edges(dot)

    def render_dot_graph(self, output):
        dot = Digraph(graph_attr={'rankdir': 'LR'})
        self.graph(dot)
        dot.render(output, view=True)

    def find(self, name):
        if self.name == name:
            return self
        else:
            for child in self.children:
                rez = child.find(name)
                if rez is not None:
                    return rez
