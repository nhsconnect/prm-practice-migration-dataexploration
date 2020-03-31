from src.concept import Concept


class Graph:
    def __init__(self, schema):
        self.types = self.gather_types(schema)

    def create_graph(self, current, prefix):
        the_name = current.attrib["name"]
        concept = Concept(the_name, prefix)

        for elem in current.iter('{http://www.w3.org/2001/XMLSchema}element'):
            elem_type = elem.attrib.get("type", "")
            if prefix in elem_type:
                concept.link_child(self.create_graph(self.types[elem_type], prefix))
            else:
                concept.link_child(Concept(the_name + "/" + elem.attrib.get("name", ""), prefix))

        return concept

    def gather_types(self, schema):
        types = {}

        for type in schema.root.iter('{http://www.w3.org/2001/XMLSchema}complexType'):
            if len(type.attrib) > 0:
                types[type.attrib['name']] = type

        return types
