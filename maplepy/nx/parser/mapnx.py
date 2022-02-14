import logging
import os

from nxpy.nxfile import NXFileSet


class MapNx:
    """
    Helper class to get values from a map nx file.

    Currently does not handle:
        reactor, ToolTip, rectInfo

    """

    def __init__(self):
        self.file = NXFileSet()

    def open(self, file):
        """ Load file from path """

        # Check if file exists
        if not os.path.exists(file):
            logging.warning(f'{file} does not exist')
            return
        try:
            # Open nx file
            self.file.load(file)
        except:
            logging.exception(f'Unable to open {file}')

    def get_values(self, node):
        """ Return the node's children as a dictionary """
        return {c.name: c.value for c in node.get_children()}

    def get_map_nodes(self):
        """ Return all available map nodes """

        map_nodes = {}

        # Loop through map indices
        for index in range(9):
            map_digit = self.file.resolve(f'Map/Map{index}')
            if map_digit:
                for child in map_digit.get_children():
                    map_nodes[child.name] = child.value

        # Return
        return map_nodes

    def get_map_node(self, map_id):
        """ Return the map node by id """
        path = f'Map/Map{map_id[0:1]}/{map_id}.img'
        return self.file.resolve(path)

    def get_info(self, map_id):
        """ Return info data for the map """

        info = {}

        # Get info node
        path = f'Map/Map{map_id[0:1]}/{map_id}.img/info'
        info_node = self.file.resolve(path)
        if not info_node:
            return None

        # Get values
        info = self.get_values(info_node)

        # Return
        return info

    def get_back(self, map_id):
        """ Return back data for the map """

        back = []

        # Get back node
        path = f'Map/Map{map_id[0:1]}/{map_id}.img/back'
        back_node = self.file.resolve(path)
        if not back_node:
            return None

        # Get values
        for node in back_node.get_children():
            values = self.get_values(node)
            values['name'] = node.name
            back.append(values)

        # Return
        return back

    def get_life(self, map_id):
        """ Return life data for the map """

        life = []

        # Get life node
        path = f'Map/Map{map_id[0:1]}/{map_id}.img/life'
        life_node = self.file.resolve(path)
        if not life_node:
            return None

        # Get values
        for node in life_node.get_children():
            values = self.get_values(node)
            values['name'] = node.name
            life.append(values)

        # Return
        return life

    def get_layer(self, map_id, index):
        """ Return layer data for the map """

        layer = {}

        # Get layer node
        path = f'Map/Map{map_id[0:1]}/{map_id}.img/{index}'
        layer_node = self.file.resolve(path)
        if not layer_node:
            return None

        # Get info for this layer
        info_node = layer_node.get_child('info')
        info = self.get_values(info_node)

        # Get tiles for this layer
        tiles = []
        tile_node = layer_node.get_child('tile')
        for node in tile_node.get_children():
            values = self.get_values(node)
            values['name'] = node.name
            tiles.append(values)

        # Get objects for this layer
        objects = []
        object_node = layer_node.get_child('obj')
        for node in object_node.get_children():
            values = self.get_values(node)
            values['name'] = node.name
            objects.append(values)

        # Return
        layer = {'info': info, 'tile': tiles, 'obj': objects}
        return layer

    def get_foothold(self, map_id):
        """ Return foothold data for the map """

        foothold = {}

        # Get foothold node
        path = f'Map/Map{map_id[0:1]}/{map_id}.img/foothold'
        foothold_node = self.file.resolve(path)
        if not foothold_node:
            return None

        # Get values
        for layer in foothold_node.get_children():
            for array in layer.get_children():
                group = []
                for node in array.get_children():
                    values = self.get_values(node)
                    values['name'] = node.name
                    group.append(values)
                foothold[f'{layer.name}/{array.name}'] = group

        # Return
        return foothold

    def get_ladder(self, map_id):
        """ Return ladder rope data for the map """

        ladder = {}

        # Get ladderRope node
        path = f'Map/Map{map_id[0:1]}/{map_id}.img/ladderRope'
        ladder_node = self.file.resolve(path)
        if not ladder_node:
            return None

        # Get values
        for node in ladder_node.get_children():
            values = self.get_values(node)
            values['name'] = node.name
            ladder[node.name] = values

        # Return
        return ladder

    def get_seat(self, map_id):
        """ Return seat data for the map """

        seat = {}

        # Get seat node
        path = f'Map/Map{map_id[0:1]}/{map_id}.img/seat'
        seat_node = self.file.resolve(path)
        if not seat_node:
            return None

        # Get values
        seat = self.get_values(seat_node)

        # Return
        return seat

    def get_minimap(self, map_id):
        """ Return mini map data for the map """

        minimap = {}

        # Get miniMap node
        path = f'Map/Map{map_id[0:1]}/{map_id}.img/miniMap'
        minimap_node = self.file.resolve(path)
        if not minimap_node:
            return None

        # Get values
        minimap = self.get_values(minimap_node)
        minimap['canvas_image'] = minimap_node['canvas'].get_image()

        # Return
        return minimap

    def get_portal(self, map_id):
        """ Return portal data for the map """

        portal = []

        # Get portal node
        path = f'Map/Map{map_id[0:1]}/{map_id}.img/portal'
        portal_node = self.file.resolve(path)
        if not portal_node:
            return None

        # Get values
        for node in portal_node.get_children():
            values = self.get_values(node)
            values['name'] = node.name
            portal.append(values)

        # Return
        return portal
