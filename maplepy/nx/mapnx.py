import logging
import os

from nx.nxfileset import NXFileSet


class MapNx:
    """ Helper class to get values from a map nx file. """

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
        return {c.name: c.value for c in node.getChildren()}

    def get_map_nodes(self):
        """ Return all available map nodes """

        map_nodes = {}

        # Loop through map indices
        for i in range(0, 9):
            map_digit = self.file.resolve(f'Map/Map{i}')
            if map_digit:
                for child in map_digit.getChildren():
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
        for node in back_node.getChildren():
            values = self.get_values(node)
            values['name'] = node.name
            back.append(values)

        # Return
        return back

    def get_life(self, map_id):
        """ Return life data for the map """

        life = []

        # Get portal node
        path = f'Map/Map{map_id[0:1]}/{map_id}.img/life'
        life_node = self.file.resolve(path)
        if not life_node:
            return None

        # Get values
        for node in life_node.getChildren():
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
        info_node = layer_node.getChild('info')
        info = self.get_values(info_node)

        # Get tiles for this layer
        tiles = []
        tile_node = layer_node.getChild('tile')
        for node in tile_node.getChildren():
            values = self.get_values(node)
            values['name'] = node.name
            tiles.append(values)

        # Get objects for this layer
        objects = []
        object_node = layer_node.getChild('obj')
        for node in object_node.getChildren():
            values = self.get_values(node)
            values['name'] = node.name
            objects.append(values)

        # Return
        layer = {'info': info, 'tile': tiles, 'obj': objects}
        return layer

    def get_reactor(self, map_id):
        """ Return reactor data for the map """
        pass

    def get_foothold(self, map_id):
        """ Return foothold data for the map """

        foothold = {}

        # Get foothold node
        path = f'Map/Map{map_id[0:1]}/{map_id}.img/foothold'
        foothold_node = self.file.resolve(path)
        if not foothold_node:
            return None

        # Get values
        for layer in foothold_node.getChildren():
            for array in layer.getChildren():
                group = []
                for node in array.getChildren():
                    values = self.get_values(node)
                    values['name'] = node.name
                    group.append(values)
                foothold[f'{layer.name}/{array.name}'] = group

        # Return
        return foothold

    def get_ladder(self, map_id):
        """ Return ladder rope data for the map """

        ladder = {}

        # Get minimap node
        path = f'Map/Map{map_id[0:1]}/{map_id}.img/ladderRope'
        ladder_node = self.file.resolve(path)
        if not ladder_node:
            return None

        # Get values
        for node in ladder_node.getChildren():
            values = self.get_values(node)
            values['name'] = node.name
            ladder[node.name] = values

        # Return
        return ladder

    def get_minimap(self, map_id):
        """ Return mini map data for the map """

        minimap = {}

        # Get minimap node
        path = f'Map/Map{map_id[0:1]}/{map_id}.img/miniMap'
        minimap_node = self.file.resolve(path)
        if not minimap_node:
            return None

        # Get values
        minimap = self.get_values(minimap_node)
        minimap['canvas_image'] = minimap_node['canvas'].getImage()

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
        for node in portal_node.getChildren():
            values = self.get_values(node)
            values['name'] = node.name
            portal.append(values)

        # Return
        return portal
