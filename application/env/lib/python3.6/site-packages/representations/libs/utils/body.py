from representations.bin.abstract_serializable import AbstractSerializable


class Body(object):

    def __init__(self, types_description=None):
        """
        :param types_description:
        :return:
        """
        types_description = types_description or dict()
        self._map = dict()
        for k, v in types_description.items():

            if k not in ('list', 'str'):
                raise TypeError('Cannot parse "{}" type'.format(k))

            self._map.update({i: k for i in v})
        self._container = dict()

    def append(self, element):
        if hasattr(element, 'items') and not isinstance(element, AbstractSerializable):
            for key, value in element.items():
                self._append_one(key.lower(), value)
        else:
            element = element if hasattr(element, '__iter__') and not \
                isinstance(element, AbstractSerializable) else (element, )
            for e in element:
                self._append_one(e.obj_name.lower(), e)
        return self

    def _append_one(self, key, value):
        action_map = {
            'list': lambda k, v: self._container[key].append(value) if
                                key in self._container else self._container.update(
                {k: value if isinstance(value, (tuple, list)) else [value, ]}
            ),
            'str': lambda k, v: self._container.update({k: v})
        }
        action_map[self._map.get(key, 'str')](key, value)
        return self

    @property
    def content(self):
        return self._container

    def __getattr__(self, item):
        try:
            return self._container[item]
        except KeyError:
            raise AttributeError('"{}" has no attribute "{}"'   .format(type(self).__name__, item))

    def __iter__(self):
        for key in self._container.keys():
            yield key

    def __len__(self):
        return len(self._container)

    def items(self):
        return self.content.items()

    def keys(self):
        return self._container.keys()


