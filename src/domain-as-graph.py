import xmlschema

from src.graph import Graph


def render_dot_graph(xsd, prefix, node_name, output):
    schema = xmlschema.XMLSchema(xsd)
    main_element = schema.root.find('{http://www.w3.org/2001/XMLSchema}complexType')
    concept = Graph(schema).create_graph(main_element, prefix)

    concept.find(node_name).render_dot_graph('../data/exports/%s' % output)


render_dot_graph('../data/OpenHR001.xsd', "OpenHR001", "OpenHR001.Patient", 'supplier-patient')
render_dot_graph('../data/OpenHR001.xsd', "OpenHR001", "OpenHR001.AdminDomain", 'supplier-admin-domain')
render_dot_graph('../data/OpenHR001.xsd', "OpenHR001", "OpenHR001.HealthDomain", 'supplier-health-domain')

render_dot_graph('../data/patient.xsd.xml', "Patient", "Patient", '../data/exports/test-fhir.gv')
