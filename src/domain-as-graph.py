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

    def link_child(self, rel_name, other_concept):
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


def create_graph(current):
    print(current.attrib)
    the_name = current.attrib["name"]
    concept = Concept(the_name)

    for elem in current.iter('{http://www.w3.org/2001/XMLSchema}element'):
        print(elem.items())
        elem_type = elem.attrib.get("type", "")
        if "OpenHR001" in elem_type:
            concept.link_child("has", create_graph(types[elem_type]))
        else:
            concept.link_child("has", Concept(the_name + "/" + elem.attrib.get("name", "")))

    return concept

schema = xmlschema.XMLSchema('../data/OpenHR001.xsd')

openHR = schema.root.find('{http://www.w3.org/2001/XMLSchema}complexType')

for type in schema.root.iter('{http://www.w3.org/2001/XMLSchema}complexType'):
    if len(type.attrib) > 0:
        types[type.attrib['name']] = type


concept = create_graph(openHR)

dot = Digraph(comment='EMIS')

concept.graph(dot)
dot.render('../data/exports/test.gv', view=True)

print(dot.source)