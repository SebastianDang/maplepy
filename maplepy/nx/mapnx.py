import os
import nx.nxfile as nxfile


class MapNx:

    """ Helper class to get values from a map nx file. """

    def __init__(self):
        self.file = None

    def open(self, file):
        # Check if file exists
        if not os.path.exists(file):
            print('{} does not exist'.format(file))
            return
        try:
            # Open nx file
            file = nxfile.NXFile(file)
            self.file = file
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

    def get_info_data(self, map_id):
        info = {}
        img = "Map/Map{}/{}.img".format(map_id[0:1], map_id)
        # Get map node
        map_node = self.file.resolve(img)
        if not map_node:
            return None
        info_node = map_node.getChild('info')
        for name in info_node.listChildren():
            info[name] = info_node.getChild(name).value
        return info

    def get_background_data(self, map_id):
        back = []
        img = "Map/Map{}/{}.img".format(map_id[0:1], map_id)
        # Get map node
        map_node = self.file.resolve(img)
        if not map_node:
            return None
        # Get the current back node
        back_node = map_node.getChild('back')
        if not back_node:
            return None
        # Get values
        for index in back_node.listChildren():
            array_node = back_node.getChild(index)
            data = {'name': index}
            for name in array_node.listChildren():
                data[name] = array_node.getChild(name).value
            back.append(data)
        return back

    def get_layer_data(self, map_id, index):
        layer = {}
        img = "Map/Map{}/{}.img".format(map_id[0:1], map_id)
        # Get map node
        map_node = self.file.resolve(img)
        if not map_node:
            return None
        # Get the current layer
        layer_node = map_node.getChild(str(index))
        if not layer_node:
            return None
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
        layer = {'info': info, 'tile': tiles, 'obj': objects}
        return layer

    def get_data(self, path):
        data = {}
        node = self.file.resolve(path)
        for name in node.listChildren():
            data[name] = node.getChild(name).value
        return data
