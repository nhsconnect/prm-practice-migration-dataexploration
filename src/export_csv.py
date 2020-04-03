import xmlschema
import csv
import xlsxwriter


class Section:
    def __init__(self, name, fields):
        self.name = name.replace("OpenHR001.","")
        self.fields = fields

    def toCsv(self):
        with open('../data/csvs/'+self.name+'.csv', mode='w') as file:
            fieldnames = ["name", "type", "description", "cardinality", "matching", "notes", "to follow up"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            for field in self.fields:
                writer.writerow({
                    "name": field.name,
                    "type": field.type,
                    "description": field.description,
                    "cardinality": field.cardinality,
                    "matching": "",
                    "notes": "",
                    "to follow up": ""
                })

    def toXlsx(self, workbook):
        if len(self.fields) == 0:
            return

        header_format = workbook.add_format({"bold": True, "font_size": "18"})
        cell_format = workbook.add_format({"font_size": "14", "valign":"vcenter", "text_wrap": "true"})
        worksheet = workbook.add_worksheet(name=self.name)
        worksheet.set_column(0, 0, 30)
        worksheet.set_column(1, 1, 40)
        worksheet.set_column(2, 2, 60)
        worksheet.set_column(3, 3, 20)
        worksheet.set_column(4, 4, 30)
        worksheet.set_column(5, 5, 50)
        worksheet.set_column(6, 6, 50)
        fieldnames = ["Name", "Type", "Description", "Cardinality", "Matching", "Notes"]

        i = 0
        worksheet.write(0,0,"Matching profile:", header_format)
        worksheet.set_row(0, 20)
        worksheet.set_row(1, 30)
        for fieldname in fieldnames:
            worksheet.write(1,i, fieldname, header_format)
            i+=1
        i=2


        for field in self.fields:
            height = (len(field.description)/60) * 25 + 20
            worksheet.set_row(i, height)
            worksheet.write(i,0, field.name,cell_format)
            worksheet.write(i,1, "internal:"+field.type+"!A1", cell_format, field.type)
            worksheet.write(i,2, field.description,cell_format)
            worksheet.write(i,3, field.cardinality,cell_format)
            worksheet.write(i,4, "",cell_format)
            worksheet.write(i,5, "",cell_format)
            i+=1


class Field:
    def __init__(self, name, type, description, cardinality):
        self.cardinality = cardinality.toS()
        self.description = description
        self.type = type.replace("OpenHR001.","") if type != None else ""
        self.name = name

class Cardinality:
    def __init__(self, min =1, max=1):
        self.min = min
        self.max = max

    def toS(self):
        return str(self.min) + " - " + str(self.max)

schema = xmlschema.XMLSchema('../data/OpenHR001.xsd')
main_element = schema.root.find('{http://www.w3.org/2001/XMLSchema}complexType')


def create_export(elem, elem_type, workbook):
    fields = []
    for child in elem.iter('{http://www.w3.org/2001/XMLSchema}element'):
        name = child.attrib.get("name")
        type = child.attrib.get("type")
        min = child.attrib.get("minOccurs")
        max = child.attrib.get("maxOccurs")
        cardinality = Cardinality(min if min != None else 1, max if max != None else 1)
        annotation = child.find('{http://www.w3.org/2001/XMLSchema}annotation')
        description = "-"
        if annotation != None:
            description = annotation.find('{http://www.w3.org/2001/XMLSchema}documentation').text

        fields.append(Field(name, type, description, cardinality))
    section = Section(elem_type, fields)
    section.toXlsx(workbook)
    return section

sections = {}
workbook = xlsxwriter.Workbook('../data/emis-gap-analysis.xlsx')

for elem in schema.root.iter('{http://www.w3.org/2001/XMLSchema}complexType'):
    elem_type = elem.attrib.get("name", "")
    sections[elem_type] = create_export(elem, elem_type, workbook)

workbook.close()

