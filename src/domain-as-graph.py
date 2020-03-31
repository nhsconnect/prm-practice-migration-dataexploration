import xmlschema

from src.graph import Graph


def render_dot_graph(xsd, prefix, node_name, output, depth=1000):
    concept = get_root(xsd, prefix)

    concept.find(node_name).render_dot_graph(output, depth=depth)


def get_root(xsd, prefix):
    schema = xmlschema.XMLSchema(xsd)
    main_element = schema.root.find('{http://www.w3.org/2001/XMLSchema}complexType')
    concept = Graph(schema).create_graph(main_element, prefix)
    return concept


def render_for_tree(path, prefix, node, depth = 1000):
    render_dot_graph(path, prefix, prefix + "." + node, '../data/exports/%s/%s' % (prefix, node), depth)


root = get_root('../data/OpenHR001.xsd', "OpenHR001")


def output_location(name):
    return '../data/exports/OpenHR001/%s' % name.replace("/", "-")


def render_2_levels_down():
    for child in root.children:
        child.render_dot_graph(output_location(child.name), 1)

        for grandchild in child.children:
            grandchild.render_dot_graph(output_location(grandchild.name), 1)
    render_for_tree('../data/OpenHR001.xsd', "OpenHR001", "OpenHealthRecord", 2)


# render_2_levels_down()
# Exaamples
render_for_tree('../data/OpenHR001.xsd', "OpenHR001", "Encounter")
# render_dot_graph('../data/OpenHR001.xsd', "OpenHR001", "OpenHR001.HealthDomain", 'supplier-health-domain')

# render_dot_graph('../data/patient.xsd.xml', "Patient", "Patient", '../data/exports/test-fhir.gv')
