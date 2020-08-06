import xml.etree.ElementTree as ET


class Map_xml:

    def __init__(self):
        self.root = None
        self.name = None
        self.info = None
        self.all_backs = None
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

        try:

            # Set name
            self.name = self.root.get('name')

            # Imgdirs
            for child in self.root:
                imgdir_name = child.get('name')
                # Info
                if imgdir_name == 'info':
                    self.parse_info(child)
                # Background images
                if imgdir_name == 'back':
                    self.parse_back(child)
                # Life
                if imgdir_name == 'life':
                    pass
                # Digit
                if imgdir_name.isdigit():
                    self.parse_digit_arrays(child)
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

        except:
            print('Error while parsing root.')

    def parse_info(self, parent):
        """
        Parse info node and store in class variable

        Args:
            parent (xml node): Xml node at 'info'
        """
        try:
            info = {}
            value_tags = ['int', 'string', 'float']
            for child in parent:
                if child.tag in value_tags:
                    info[child.get('name')] = child.get('value')
            self.info = info
        except Exception:
            print('Error while parsing info.')

    def parse_back(self, parent):
        """
        Parse background image nodes and store in class variable

        Args:
            parent (xml node): Xml node at 'back'
        """
        try:
            back = []
            value_tags = ['int', 'string']
            for child in parent:
                back_value = {}
                back_value['name'] = child.attrib.get('name')
                for value in child:
                    if value.tag in value_tags:
                        back_value[value.get('name')] = value.get('value')
                back.append(back_value)
            self.all_backs = back
        except Exception:
            print('Error while parsing bg.')

    def parse_digit_arrays(self, parent):
        """
        Parse individual arrays that begins with digits,
        containing tiles and objs

        Args:
            parent (xml node):  Xml node at digit arrays
        """
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
                    child[:] = sorted(
                        child, key=lambda c: (c.tag, c.get('name')))
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
            self.all_tiles.append({"info": info, "tiles": tiles})
            self.all_objects.append({"info": info, "objects": objects})
        except Exception:
            print('Error while parsing digit arrays.')
