from representations.bin.abstract_serializable import AbstractSerializable
from representations.libs.exceptions import SirenDumpException
from representations.libs.utils.body import Body

__author__ = 'atomikin'


class SirenObjectAPI(AbstractSerializable):

    def check_input(self, params):
        limited = sum([1 for k, v in params.items() if k in self.LIMITED]) == len(params) if self.LIMITED else True
        keys = params.keys()
        required = sum([1 for i in self.REQUIRED if i in keys]) == len(self.REQUIRED)
        return limited, required

    @property
    def body(self):
        try:
            return self._body
        except AttributeError:
            self._body = Body()
            return self._body

    @property
    def obj_name(self):
        try:
            return self._class
        except AttributeError as err:
            return type(self).__name__.lstrip('Dy_')

    @property
    def _dict(self):
        res = dict()
        check_result = self.check_input(self.content)
        if not sum(check_result) == len(check_result):
            err_msg = 'Provided keys "{}", while should be in "{}", where "{}" are required.'.format(
                self.content.keys(),
                self.LIMITED,
                self.REQUIRED
            )
            raise SirenDumpException(err_msg)
        for k, v in self.content.items():
            if isinstance(v, (list, tuple)):
                l = list()
                for i in v:
                    if isinstance(i, SirenObjectAPI):
                        l.append(i._dict)
                    else:
                        l.append(i)
                res[k] = l
            elif isinstance(v, SirenObjectAPI):
                res[k] = v._dict
            else:
                res[k] = v
        return res

    @property
    def classes(self):
        return self.content['class']

    @classmethod
    def create(cls, *args, mixins=tuple(), **kwargs):
        return cls.plug(mixins)(*args, **kwargs)

    def __getattr__(self, item):
        if item != '_body':
            return getattr(self.body, item)
        raise AttributeError()

    @classmethod
    def plug(cls, mixins=tuple()):
        if cls.IMPLEMENTATION and cls.IMPLEMENTATION not in mixins:
            mixins = tuple(mixins) + (cls.IMPLEMENTATION,)
        if mixins:
            return type('Dy_{}'.format(cls.__name__), (cls,) + tuple(mixins), dict())
        return cls



