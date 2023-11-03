from representations.bin.link import Link
from representations.bin.siren_object import SirenObject


class Entity(SirenObject):

    def __init__(self, *args, **kwargs):
        # representation.body.append(Class('Collection'))
        self._class = 'entities'


class EmbeddedLink(Link, Entity):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._class = 'entities'

