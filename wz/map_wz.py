import xml.etree.ElementTree as ET


class map_wz:

    def __init__(self):
        self.root = None
        self.info = None
        self.bg = None
        self.all_tiles = []
        self.all_objects = []

    def open(self, file):
        """
        Open MapleStory xml file

        Args:
            file (xml): MapleStory xml file
        """
        if self.root:
            print('Xml file already opened.')
            return
        self.root = ET.parse(file).getroot()

    def parse_root(self):
        """
        Parse MapleStory xml file
        """
        if not self.root:
            print('No xml file opened.')
            return

        print('Parsing root')
        try:
            # Top level wz img
            wzimg = self.root.find('wzimg')

            # Imgdirs
            for imgdir in wzimg.findall('imgdir'):
                imgdir_name = imgdir.get('name')
                # Info
                if imgdir_name == 'info':
                    self.parse_info(imgdir)
                # Background images
                if imgdir_name == 'back':
                    self.parse_bg(imgdir)
                # Life
                if imgdir_name == 'life':
                    pass
                # Digit
                if imgdir_name.isdigit():
                    self.parse_tile_set(imgdir)
                # Reactor
                if imgdir_name == 'reactor':
                    pass
                # ToolTip
                if imgdir_name == 'ToolTip':
                    pass
                # RectInfo
                if imgdir_name == 'rectInfo':
                    pass
                # Foothold
                if imgdir_name == 'foothold':
                    pass
                # Ladder/Ropes
                if imgdir_name == 'ladderRope':
                    pass
                # Seat
                if imgdir_name == 'seat':
                    pass
                # Mini map
                if imgdir_name == 'miniMap':
                    pass
                # Portal
                if imgdir_name == 'portal':
                    pass

            self.all_tiles = sorted(self.all_tiles, key=lambda k: k['zM'])
            self.all_objects = sorted(self.all_objects, key=lambda k: k['zM'])

            print('Done!')

        except Exception:
            print('Error while parsing root.')

    def parse_info(self, parent):
        """
        Parse info node and store in class variable

        Args:
            parent (xml node): Xml node at 'info'
        """
        print('Parsing info')
        try:
            info = {}
            value_tags = ['int', 'string', 'float']
            for child in parent:
                if child.tag in value_tags:
                    info[child.get('name')] = child.get('value')
            self.info = info
        except Exception:
            print('Error while parsing info.')

    def parse_bg(self, parent):
        """
        Parse background image nodes and store in class variable

        Args:
            parent (xml node): Xml node at 'back'
        """
        print('Parsing bg')
        try:
            bg = []
            value_tags = ['int', 'string']
            for child in parent:
                bg_value = {}
                bg_value['name'] = child.attrib.get('name')
                for value in child:
                    if value.tag in value_tags:
                        bg_value[value.get('name')] = value.get('value')
                bg.append(bg_value)
            self.bg = bg
        except Exception:
            print('Error while parsing info.')

    def parse_tile_set(self, parent):
        """
        Parse individual tile sets

        Args:
            parent (xml node):  Xml node at tile num
        """
        print('Parsing tile set')
        try:
            info = {}
            tiles = []
            objects = []
            value_tags = ['int', 'string']
            for child in parent:
                if child.attrib.get('name') == 'info':
                    for value in child:
                        info[value.get('name')] = value.get('value')
                if child.attrib.get('name') == 'tile':
                    child[:] = sorted(child, key=lambda c: (c.tag,c.get('name')))
                    for subchild in child:
                        tile = {}
                        for value in subchild:
                            tile['info'] = info
                            if value.tag in value_tags:
                                tile[value.get('name')] = value.get('value')
                        tiles.append(tile)
                if child.attrib.get('name') == 'obj':
                    for subchild in child:
                        obj = {}
                        for value in subchild:
                            obj['info'] = info
                            if value.tag in value_tags:
                                obj[value.get('name')] = value.get('value')
                        objects.append(obj)
            self.all_tiles += tiles
            self.all_objects += objects
        except Exception:
            print('Error while parsing info.')


if __name__ == "__main__":
    print(map_wz.__name__)
    m = map_wz()
    m.open('./xml/000010000.xml')
    m.parse_root()
