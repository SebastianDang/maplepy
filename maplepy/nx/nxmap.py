import os
import nx.nxfile as nxfile


class NXMap:

    """ Helper class to get values from a map nx file. """

    def __init__(self):
        self.file = None
        self.maps = None

    def open(self, file):
        # Check if file exists
        if not os.path.exists(file):
            print('{} does not exist'.format(file))
            return
        try:
            # Open nx file
            file = nxfile.NXFile(file)
            # Get root node
            root = file.getRoot()
            # Get all map nodes
            map_nodes = self.get_map_nodes(root.getChild('Map'))
            self.maps = map_nodes  # If reading fails, None
        except:
            print('Unable to open {}'.format(file))

    def get_map_nodes(self, map_root):
        map_nodes = {}
        for i in range(0, 9):
            map_digit = map_root.getChild('Map{}'.format(i))
            if not map_digit:
                continue
            for map_id in map_digit.listChildren():
                node = map_digit.getChild(map_id)
                if not node:
                    continue
                map_nodes[map_id] = node
        return map_nodes

    def get_map_list(self):
        if self.maps:
            return [k for k, v in self.maps.items()]

    def get_info_data(self, map_id):
        info = {}
        img = '{}.img'.format(map_id)
        if self.maps and img in self.maps:
            map_node = self.maps[img]
            info_node = map_node.getChild('info')
            for name in info_node.listChildren():
                info[name] = info_node.getChild(name).value
        return info

    def get_background_data(self, map_id):
        back = []
        img = '{}.img'.format(map_id)
        if self.maps and img in self.maps:
            map_node = self.maps[img]
            back_node = map_node.getChild('back')
            for index in back_node.listChildren():
                array_node = back_node.getChild(index)
                data = {'name': index}
                for name in array_node.listChildren():
                    data[name] = array_node.getChild(name).value
                back.append(data)
        return back

    def get_tile_object_data(self, map_id):
        tile_object_layers = []
        img = '{}.img'.format(map_id)
        if self.maps and img in self.maps:
            map_node = self.maps[img]
            for i in range(0, 8):
                # Get the current layer
                layer_node = map_node.getChild('{}'.format(i))
                if not layer_node:
                    continue
                # Get info for this layer
                info = {}
                info_node = layer_node.getChild('info')
                for name in info_node.listChildren():
                    info[name] = info_node.getChild(name).value
                # Get tiles for this layer
                tiles = []
                tile_node = layer_node.getChild('tile')
                for index in tile_node.listChildren():
                    array_node = tile_node.getChild(index)
                    data = {'name': index}
                    for name in array_node.listChildren():
                        data[name] = array_node.getChild(name).value
                    tiles.append(data)
                # Get objects for this layer
                objects = []
                object_node = layer_node.getChild('obj')
                for index in object_node.listChildren():
                    array_node = object_node.getChild(index)
                    data = {'name': index}
                    for name in array_node.listChildren():
                        data[name] = array_node.getChild(name).value
                    objects.append(data)
                # Add layer
                tile_object_layers.append(
                    {'info': info, 'tile': tiles, 'obj': objects})
        return tile_object_layers
