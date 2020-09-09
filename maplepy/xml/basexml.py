import logging
import os
import xml.etree.ElementTree as ET
from enum import Enum


class Layer(Enum):
    """Enum used to parse xmls by type"""
    TAGS = 1
    CANVAS_ARRAY = 2


class BaseXml:
    """
    Basic xml reader for elementary items:
        Back
        Tile
        Obj
    """

    def __init__(self):
        self.root = None
        self.name = None
        self.info = None
        self.items = None

    def open(self, file):
        if self.root:
            logging.info(f'{file} already opened.')
            return
        if not os.path.isfile(file):
            logging.warning(f'{file} does not exist.')
            return
        self.root = ET.parse(file).getroot()

    def parse_root(self, layer):
        """Parse the xml file beginning at root."""

        if not self.root:
            logging.warning('No file opened.')
            return

        try:

            info = {}
            items = {}

            # Parse xml
            for child in self.root:

                # A single list of values
                if child.attrib.get('name') == 'info':
                    info = self.parse_info(child)

                # Nested values
                else:

                    # Start at tags
                    if layer == Layer.TAGS:
                        items[child.get('name')] = self.parse_tags(child)

                    # Start at canvases
                    elif layer == Layer.CANVAS_ARRAY:
                        items[child.attrib.get(
                            'name')] = self.parse_canvas_array(child)

            # Set variables
            self.name = self.root.get('name')
            self.info = info
            self.items = items

        except:
            logging.exception('Error while parsing.')

    def parse_info(self, info):
        """
        <imgdir name="info"/>
            <int/>
            <string/>
        </imgdir>
        """

        item = {}
        value_tags = ['int', 'string']
        for value in info:
            if value.tag in value_tags:
                item[value.get('name')] = value.get('value')
        return item

    def parse_tags(self, tags):
        """
        <imgdir>
            <imgdir/>
            ...
            <imgdir/>
        </imgdir>
        """

        items = {}
        for child in tags:
            items[child.get('name')] = self.parse_item_array(child)
        return items

    def parse_item_array(self, array):
        """
        <imgdir>
            <imgdir/>
            ...
            <imgdir/>
        </imgdir>
        """

        items = []
        for child in array:
            items.append(self.parse_canvas_array(child))
        return items

    def parse_canvas_array(self, canvases):
        """
        <imgdir>
            <canvas/>
            ...
            <canvas/>
        </imgdir>
        """

        items = []
        for child in canvases:
            items.append(self.parse_canvas(child))
        return items

    def parse_canvas(self, canvas):
        """
        <canvas>
            <extended/>
            <vector/>
            <int/>
            <string/>
        </canvas>
        """

        item = {}
        extended_tags = ['extended']
        vector_tags = ['vector']
        value_tags = ['int', 'string']
        item['name'] = canvas.get('name')
        item['width'] = canvas.get('width')
        item['height'] = canvas.get('height')
        for value in canvas:
            if value.tag in extended_tags:
                item['extended'] = self.parse_extended(value)
            if value.tag in vector_tags:
                item['x'] = value.get('x')
                item['y'] = value.get('y')
            if value.tag in value_tags:
                item[value.get('name')] = value.get('value')
        return item

    def parse_extended(self, extended):
        """
        <extended>
            <vector/>
            ...
            <vector/>
        </extended>
        """

        items = []
        vector_tags = ['vector']
        for value in extended:
            item = {}
            item['name'] = value.get('name')
            if value.tag in vector_tags:
                item['x'] = value.get('x')
                item['y'] = value.get('y')
            items.append(item)
        return items
