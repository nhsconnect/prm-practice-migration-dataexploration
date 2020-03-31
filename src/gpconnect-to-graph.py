import xml.etree.ElementTree as ET

from src.concept import Concept


def render_graph(path, profile, output, depth = 1000):
    tree = ET.parse(path)
    root = tree.getroot()
    print(root)
    concepts = {}
    for elem in root.find("{http://hl7.org/fhir}snapshot").iter("{http://hl7.org/fhir}element"):
        parts = elem.attrib["id"].split(".")

        no_of_parts = len(parts)
        part = elem.attrib["id"]

        part = part.replace(":", ">")
        if part in concepts:
            current = concepts[part]
        else:
            current = Concept(part, profile)
            concepts[part] = current

        if no_of_parts > 1:
            parent_name = part.rpartition(".")[0]
            parent = concepts[parent_name]
            parent.link_child(current)

    print(concepts[profile])
    concepts[profile].render_dot_graph(output, depth)


# render_graph('../data/gpconnect-patient.xml', "Patient", "../data/exports/GPConnect/gpconnect-patient-depth-2", 2)
render_graph('../STU3-FHIR-Assets/StructureDefinitions/CareConnect-GPC-Encounter-1.xml', "Encounter", "../data/exports/GPConnect/gpconnect-encounter")
render_graph('../STU3-FHIR-Assets/StructureDefinitions/CareConnect-GPC-Appointment-1.xml', "Appointment", "../data/exports/GPConnect/gpconnect-appointment")