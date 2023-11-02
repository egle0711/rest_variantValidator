from representations.bin.siren_object import SirenObject
from representations.libs.utils.body import Body


class Link(SirenObject):

    REQUIRED = ('rel', 'href')
    LIMITED = REQUIRED + ('title', 'type', 'class')

    def __init__(self, **kwargs):
        self._class = 'links'
        self._body = Body(types_description={'str': ('href', 'title', 'type'), 'list': ('class', 'rel')})
        self.body.append(kwargs)




