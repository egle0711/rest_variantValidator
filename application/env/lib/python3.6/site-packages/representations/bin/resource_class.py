from representations.bin.siren_object import SirenObject


class Class(SirenObject):

    def __init__(self, cl):
        self._class = 'class'
        self._content = cl

    @property
    def content(self):
        return self._content

    def dump(self, indent=None):
        raise NotImplementedError()

    @classmethod
    def load(cls, serialized: str):
        raise NotImplementedError()

