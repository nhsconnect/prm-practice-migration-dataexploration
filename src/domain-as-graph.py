import xmlschema
from graphviz import Digraph

print("Hello")

types = {}


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

    def find(self, name):
        if self.name == name:
            return self
        else:
            for child in self.children:
                rez = child.find(name)
                if rez is not None:
                    return rez


def create_graph(current):
    print(current.attrib)
    the_name = current.attrib["name"]
    concept = Concept(the_name)

    for elem in current.iter('{http://www.w3.org/2001/XMLSchema}element'):
        print(elem.items())
        elem_type = elem.attrib.get("type", "")
        if "OpenHR001" in elem_type:
            concept.link_child(create_graph(types[elem_type]))
        else:
            concept.link_child(Concept(the_name + "/" + elem.attrib.get("name", "")))

    return concept


def render_subtree(concept, node_name, output):
    node = concept.find(node_name)
    dot = Digraph(graph_attr={'rankdir': 'LR'})
    node.graph(dot)
    dot.render('../data/exports/%s' % output, view=True)


schema = xmlschema.XMLSchema('../data/OpenHR001.xsd')

openHR = schema.root.find('{http://www.w3.org/2001/XMLSchema}complexType')

for type in schema.root.iter('{http://www.w3.org/2001/XMLSchema}complexType'):
    if len(type.attrib) > 0:
        types[type.attrib['name']] = type

concept = create_graph(openHR)

render_subtree(concept, "OpenHR001.Patient", 'supplier-patient')
render_subtree(concept, "OpenHR001.AdminDomain", 'supplier-admin-domain')
render_subtree(concept, "OpenHR001.HealthDomain", 'supplier-health-domain')