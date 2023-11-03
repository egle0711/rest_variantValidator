from abc import ABCMeta, abstractmethod


class AbstractSerializable(metaclass=ABCMeta):
    """
    API
        class constants:
            REQUIRED - identifies the required fields. If any of mentioned there
                fields are left out, the class cannot be instantiated
            LIMITED - the full list of the available attributes. If there is an
                attribute not listed there, then the class cannot be instantiated.
        class variables:
            implementation - a reference to class that implements API of AbstractSerializable

        methods:
            dump(indent:int)->str - returns a txt version of serialized into some format (JSON, XML or whatever) obj.
            loads(data: str)->AbstractSerializable: a classmethod (factory method) building the actual objects out
                of the txt representation(JSON, XML, or whatever)
    """

    REQUIRED = tuple()
    LIMITED = tuple()
    IMPLEMENTATION = None

    ########
    # abstract
    @abstractmethod
    def dump(self, indent=None) -> str:
        pass

    @classmethod
    @abstractmethod
    def load(cls, data: str):
        pass
    ########



