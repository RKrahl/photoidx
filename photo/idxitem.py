"""Provide the class IdxItem which represents an item in the index.
"""


class IdxItem(object):

    def __init__(self, filename=None, data=None):
        self.filename = None
        self.tags = []
        if data is not None:
            self.__dict__.update(data)
        elif filename is not None:
            self.filename = filename

    def as_dict(self):
        return dict(self.__dict__)
