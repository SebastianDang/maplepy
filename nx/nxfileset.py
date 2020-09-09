import logging
import os

from nx.nxfile import NXFile


class NXFileSet:
    """ Create a set of nx files that share data """

    def __init__(self, *argv):

        self.nxfiles = []
        for arg in argv:
            self.load(arg)

    def load(self, path):

        # Check if path exists before adding
        if not os.path.exists(path):
            logging.warning(f'{path} does not exist')
            return

        # Create nx file, set parent to self
        self.nxfiles.append(NXFile(path=path, parent=self))

    def resolve(self, path):

        # Attempt to resolve until success
        for nxfile in self.nxfiles:
            node = nxfile.resolve(path)
            if node:
                return node

        return None
