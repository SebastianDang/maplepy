import xml.etree.ElementTree as ET


class Tile_xml:

    def __init__(self):
        self.root = None
        self.name = None
        self.info = None
        self.tiles = None

    def open(self, file):
        if self.root:
            print('Xml file already opened.')
            return
        self.root = ET.parse(file).getroot()

    def parse_root(self):
        if not self.root:
            print('No xml file opened.')
            return
        try:
            info = {}
            tiles = {}
            vector_tags = ['vector']
            value_tags = ['int', 'string']
            # Parse xml
            for child in self.root:
                if child.attrib.get('name') == 'info':
                    for value in child:
                        if value.tag in value_tags:
                            info[value.get('name')] = value.get('value')
                else:
                    tile_data = []
                    for subchild in child:
                        obj = {}
                        for value in subchild:
                            if value.tag in vector_tags:
                                obj['cx'] = value.get('x')
                                obj['cy'] = value.get('y')
                            if value.tag in value_tags:
                                obj[value.get('name')] = value.get('value')
                        tile_data.append(obj)
                    tiles[child.attrib.get('name')] = tile_data
            # Set variables
            self.name = self.root.get('name')
            self.info = info
            self.tiles = tiles
        except Exception:
            print('Error while parsing tile.')
