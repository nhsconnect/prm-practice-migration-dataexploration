import xml.etree.ElementTree as ET

from src.concept import Concept

tree = ET.parse('../data/gpconnect-patient.xml')
root = tree.getroot()
print(root)

concepts = {}

for elem in root.find("{http://hl7.org/fhir}snapshot").iter("{http://hl7.org/fhir}element"):
    parts = elem.attrib["id"].split(".")

    no_of_parts = len(parts)
    part = elem.attrib["id"]

    part = part.replace(":",">")
    if part in concepts:
        current = concepts[part]
    else:
        current = Concept(part, "Patient")
        concepts[part] = current

    if no_of_parts > 1:
        parent_name = part.rpartition(".")[0]
        parent = concepts[parent_name]
        parent.link_child(current)

print([concept.name for concept in concepts["Patient"].children])
concepts["Patient"].render_dot_graph("../data/exports/GPConnect/gpconnect-patient-depth-2", 2)