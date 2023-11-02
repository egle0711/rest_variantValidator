from representations.bin.siren_object import SirenObject
from representations.libs.utils.body import Body


class Action(SirenObject):

    REQUIRED = ('name', 'href')
    LIMITED = REQUIRED + ('title', 'type', 'method', 'fields')

    DEFAULT_TYPE = 'application/x-www-form-urlencoded'

    def __init__(self, **kwargs):
        kwargs['type'] = kwargs.get('type', self.DEFAULT_TYPE)
        self._body = Body(types_description={'list': ('fields', )})
        self.append(kwargs)
        self._class = 'actions'


class Field(SirenObject):

    REQUIRED = ('name', )
    LIMITED = REQUIRED + ('class', 'type', 'value', 'title')

    TYPES = ('hidden', 'text', 'search', 'tel',
             'url', 'email', 'password', 'datetime',
             'date', 'month', 'week', 'time', 'datetime-local',
             'number', 'range', 'color', 'checkbox, radio', 'file'
             )

    def check_input(self, params):
        limited, required = super().check_input(params)
        field_type = params.get('type')
        if field_type and field_type not in self.TYPES:
            return limited, required, False
        return limited, required, True

    def __init__(self, **kwargs):
        result = self.check_input(kwargs)[2]
        if not result:
            raise TypeError('Illegal field type: "{}". Only HTML5 types are allowed.'.format(kwargs['type']))
        self._body = Body(types_description={'list': ('class', )})
        self.append(kwargs)
        self._class = 'fields'







