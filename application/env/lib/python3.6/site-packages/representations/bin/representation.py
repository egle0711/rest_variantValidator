from representations.bin.entity import Entity
from representations.bin.siren_object import SirenObject
from representations.libs.utils.body import Body


class Representation(SirenObject):

    LIMITED = ('links', 'properties', 'actions', 'entities', 'class')
    REQUIRED = ('class', )

    def __init__(self, model=None):
        self.model = model
        self._body = self._body = Body(types_description={'list': ['links', 'entities', 'class', 'actions']})
        self.body.append({'class': self.obj_name.lstrip('Dy_')})

    def dump(self, indent=None) -> str:
        return super().dump(indent=indent)

    # @classmethod
    # def load(cls, text):
    #     loaded = super().load(text)
    #     res = cls()
    #     res.body.append(loaded)

    @classmethod
    def create(cls, *args, **kwargs):
        model = args[0]
        if isinstance(model, (list, tuple)):
            collection_csl = type('{}Collection'.format(cls.__name__), (RepresentationCollection, cls), {})
            return collection_csl.create(model)
        return super().create(model)


class EmbeddedRepresentation(Representation, Entity):
    """
    Class representing an embedded resources
    """

    def __init__(self, model):
        """
        :param resource: has to be a descendant of AbstractSerializable
        :return: self
        """
        super().__init__(model)
        self._class = 'entities'


class RepresentationCollection(Representation):

    def __init__(self, collection):
        super().__init__(collection)
        self.model = None
        self.models = collection
        t = type(self)
        t_name = t.__name__.lstrip('Dy_').replace('Collection', '')
        cls = [i for i in reversed(t.__mro__) if (i.__name__ == t_name)][0]
        # cls = type(cls.__name__, (EmbeddedRepresentation, cls,), dict())
        for r in collection:
            print(r)
            self.append({'entities': cls.create(r)})

    @classmethod
    def create(cls, *args, mixins=tuple(), **kwargs):
        if cls.IMPLEMENTATION and cls.IMPLEMENTATION not in mixins:
            mixins = tuple(mixins) + (cls.IMPLEMENTATION,)
        if mixins:
            Type = type('Dy_{}'.format(cls.__name__), (cls, ) + tuple(mixins), dict())
            obj = Type(*args)
            return obj
        else:
            return cls(*args)








