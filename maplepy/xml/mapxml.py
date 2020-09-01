import os
import logging
import xml.etree.ElementTree as ET


class MapXml:

    def __init__(self):
        self.root = None
        self.name = None
        self.info = None
        self.back_items = None
        self.life_items = None
        self.map_items = []
        self.tooltip_items = None
        self.ladder_items = None
        self.portal_items = None

    def open(self, file):
        """
        Open MapleStory xml file

        Args:
            file (xml): MapleStory xml file
        """
        if self.root:
            logging.info(f'{file} already opened.')
            return
        if not os.path.isfile(file):
            logging.warning(f'{file} does not exist.')
            return
        self.root = ET.parse(file).getroot()

    def parse_root(self):
        """
        Parse MapleStory xml file
        """
        if not self.root:
            logging.warning('No xml file opened.')
            return

        try:

            # Set name
            self.name = self.root.get('name')

            # Imgdirs
            for child in self.root:
                imgdir_name = child.get('name')
                # Info
                if imgdir_name == 'info':
                    self.info = self.parse_values(child)
                # Background images
                if imgdir_name == 'back':
                    self.back_items = self.parse_array(child)
                # Life
                if imgdir_name == 'life':
                    self.life_items = self.parse_array(child)
                # Digit
                if imgdir_name.isdigit():  # Tiles / Objects
                    self.parse_digit_arrays(child)
                # Reactor
                if imgdir_name == 'reactor':
                    pass
                # ToolTip
                if imgdir_name == 'ToolTip':
                    self.tooltip_items = self.parse_array(child)
                # RectInfo
                if imgdir_name == 'rectInfo':
                    pass
                # Foothold
                if imgdir_name == 'foothold':
                    pass
                # Ladder/Ropes
                if imgdir_name == 'ladderRope':
                    self.ladder_items = self.parse_array(child)
                # Seat
                if imgdir_name == 'seat':
                    pass
                # Mini map
                if imgdir_name == 'miniMap':
                    pass
                # Portal
                if imgdir_name == 'portal':
                    self.portal_items = self.parse_array(child)
                    pass

        except:
            logging.exception('Error while parsing root.')

    def parse_array(self, parent):
        """
        Parse array nodes and return list

        Args:
            parent (xml node): Xml parent node of array
        """
        try:
            items = []
            for child in parent:
                data = self.parse_values(child)
                data['name'] = child.attrib.get('name')
                items.append(data)
            return items
        except:
            logging.exception('Error while parsing array.')

    def parse_values(self, parent):
        """
        Parse value node and return values

        Args:
            parent (xml node): Xml parent node of values
        """
        try:
            items = {}
            value_tags = ['int', 'string', 'float']
            for child in parent:
                if child.tag in value_tags:
                    items[child.get('name')] = child.get('value')
            return items
        except:
            logging.exception('Error while parsing value.')

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
                    for subchild in child:
                        tile = {}
                        tile['name'] = subchild.get('name')
                        for value in subchild:
                            tile['info'] = info
                            if value.tag in value_tags:
                                tile[value.get('name')] = value.get('value')
                        tiles.append(tile)
                if child.attrib.get('name') == 'obj':
                    for subchild in child:
                        obj = {}
                        obj['name'] = subchild.get('name')
                        for value in subchild:
                            obj['info'] = info
                            if value.tag in value_tags:
                                obj[value.get('name')] = value.get('value')
                        objects.append(obj)
            self.map_items.append(
                {"info": info, "tiles": tiles, "objects": objects})
        except:
            logging.exception('Error while parsing digit arrays.')
