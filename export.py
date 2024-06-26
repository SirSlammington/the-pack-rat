from datetime import datetime
import xml.etree.ElementTree as ElemTree
import csv, json

class Export:
    def __init__(self, data, data_spec):
        self.data = data
        self.data_spec = data_spec

    def toTXT(self):
        # File will be named based on the time the file was created to delineate between different enumerations
        with open(f'packrat_{datetime.now().strftime("%H-%M-%S")}_{self.data_spec}_datalist.txt', 'w') as result_file:
            for item in self.data:
                result_file.write(item + '\n')
        result_file.close()

    def toXML(self):
        parent_element = ElemTree.Element(f'{self.data_spec}_data')
        for item in self.data:
            element = ElemTree.SubElement(parent_element, f'{self.data_spec}')
            element.set('type', 'entry')
            element.text = f'{item}'
        ElemTree.indent(parent_element)
        xml_bytes_data = ElemTree.tostring(parent_element)
        xml_header = b'<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n'

        with open(f'packrat_{datetime.now().strftime("%H-%M-%S")}_{self.data_spec}_datalist.xml', 'wb') as result_file:
            result_file.write(xml_header)
            result_file.write(xml_bytes_data)
        result_file.close()

    def toCSV(self):
        with open(f'packrat_{datetime.now().strftime("%H-%M-%S")}_{self.data_spec}_datalist.csv', 'w', encoding='UTF8') as result_file:
            writer = csv.writer(result_file, lineterminator=',')
            for item in self.data:
                writer.writerow([item])
        result_file.close()

    '''!!!WIP!!! This will be solved later here and in the other non-text formats to insert more data including information about the scrape itself'''
    def toJSON(self):
        dictionary_data = {f'{self.data_spec}s':self.data}
        serialized_json_data = json.dumps(dictionary_data, indent=3)
        with open(f'packrat_{datetime.now().strftime("%H-%M-%S")}_{self.data_spec}_datalist.json', 'w', encoding='UTF8') as result_file:
            result_file.write(serialized_json_data)
        result_file.close()