import os
import xml.etree.ElementTree as ET


class Object_xml:

    def __init__(self):
        self.root = None
        self.name = None
        self.objects = None

    def open(self, file):
        if self.root:
            print('{} already opened.'.format(file))
            return
        if not os.path.isfile(file):
            print('{} does not exist.'.format(file))
            return
        self.root = ET.parse(file).getroot()

    def parse_root(self):
        if not self.root:
            print('No file opened.')
            return
        try:
            objects = {}
            vector_tags = ['vector']
            value_tags = ['int', 'string']

            for child in self.root:
                objects[child.get('name')] = self.parse_tags(child)
            self.name = self.root.get('name')
            self.objects = objects

        except Exception:
            print('Error while parsing.')

    def parse_tags(self, tags):
        items = {}
        for child in tags:
            items[child.get('name')] = self.parse_item_array(child)
        return items

    def parse_item_array(self, array):
        items = []
        for child in array:
            items.append(self.parse_canvas_array(child))
        return items

    def parse_canvas_array(self, canvases):
        items = []
        for child in canvases:
            items.append(self.parse_canvas(child))
        return items

    def parse_canvas(self, canvas):
        item = {}
        vector_tags = ['vector']
        value_tags = ['int', 'string']
        # Canvas values
        item['name'] = canvas.get('name')
        item['width'] = canvas.get('width')
        item['height'] = canvas.get('height')
        # Inner items
        for value in canvas:
            if value.tag in vector_tags:
                item['cx'] = value.get('x')
                item['cy'] = value.get('y')
            if value.tag in value_tags:
                item[value.get('name')] = value.get(
                    'value')
        return item

if __name__ == "__main__":
    print(Object_xml.__name__)
    m = Object_xml()
    m.open('./data/Obj/acc1.img.xml')
    m.parse_root()
    result = m.objects.get('mapleIsland', {}).get('maple')
    result = result[0]
    print(result)