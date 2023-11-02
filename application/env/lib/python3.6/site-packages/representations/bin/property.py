from representations.bin.siren_object import SirenObject


class Property(SirenObject):

    def __init__(self, **kwargs):
        self._class = 'properties'
        self.body.append(kwargs)

