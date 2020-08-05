import xml.etree.ElementTree as ET


class map_wz:

    def __init__(self):
        self.root = None
        self.info = None
        self.bg = None

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


if __name__ == "__main__":
    print(map_wz.__name__)
    m = map_wz()
    m.open('./xml/100000000.xml')  # Henesys
    m.parse_root()
