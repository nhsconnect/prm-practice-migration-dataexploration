import xmlschema
from neo4j import GraphDatabase

print("hello")

types = {}

def remove_dots_and_slashes(name):
    return name.replace(".","dot")\
        .replace("/","slash")

class HelloWorldExample(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(encrypted= False, uri=uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def run(self, message):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run(message)
        # return result.single()[0]


class Concept:
    def __init__(self, name):
        self.name = name
        self.children = []

    def get_name(self):
        return self.name

    def link_child(self, rel_name, other_concept):
        self.children.append(other_concept)

    def path(self, tx, parent_node, level):
        self_name = self.name.replace('OpenHR001.','')
        child_level = "L"+str(level)
        tx.run("CREATE (a:" + child_level + "{name: \""+self_name+"\"})")
        tx.run("MATCH (a),(b) WHERE a.name = \""+parent_node+ "\" and b.name = \""+self_name+ "\" CREATE (a)-[r:isparentof]->(b)")
        for child in self.children:
            child.path(tx, self_name, level+1)

    def nodes(self, tx):
        node_name = self.name.replace('OpenHR001.', '')
        tx.run("CREATE (a:Domain {name: \""+node_name+"\"})")
        for child in self.children:
            child.path(tx, node_name, 1)

    def graph(self, tx):
        self.nodes(tx)
        # self.edges(tx)


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

example = HelloWorldExample('bolt://neo4j:password10@127.0.0.1:7687', 'neo4j', 'password10')

concept.graph(example)

#example.print_greeting("some message")