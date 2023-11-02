import pytest

from representations.bin.link import Link
from representations.bin.property import Property
from representations.bin.representation import Representation
from representations.tests.fixtures import *


class NewRepresentation(Representation):
    def __init__(self, model=None):
        super().__init__(model=model)
        if not isinstance(model, (list, tuple)):
            self.append(Link.create(rel='self',
                                    href='http://localhost:3000/master/{}/items/{}'.format(model.model.id, model.id)))
            ac = Action.create(
                name='test-action',
                href='http://localhost:3000/master/{}/items/{}'.format(model.model.id, model.id)
            )
            ac.append(Field.create(name='number', value=1))
            self.append(ac)
        elif model:
            self.append(Link.create(rel='self',
                                    href='http://localhost:3000/master/{}'.format(model[0].id)))
            self.append(Property.create(size=10, page=1))


class MasterRepresentation(Representation):
    def __init__(self, model=None):
        super().__init__(model=None)
        self.append({'entities': [NewRepresentation.create(i) for i in model.related_models]})
        self.append(Link.create(rel='self', href='http://localhost:3000/master/{}'.format(model.id)))


class TestRepresentation:

    def test_create_method(self, prepare_models, prepare_action):
        model = prepare_models
        rep = MasterRepresentation.create(model)
        rep.append(prepare_action)

        assert rep
        assert rep.dump(indent=1)
        assert 'links' in rep.content
        assert 'entities' in rep.content
        assert len(rep.entities) == len(prepare_models.related_models)
        assert 'class' in rep.content


class TestRepresentationCollection:
    def test_create_collection(self, prepare_models):
        models = prepare_models.related_models
        rep = NewRepresentation.create(models)
        assert 'properties' in rep.content
        assert rep.properties.size == 10
        assert rep.properties.page == 1
        assert rep.entities.__len__() == prepare_models.related_models.__len__()
        assert rep.links.__len__() == 1
        assert rep.entities[0].links.__len__() == 1
        assert rep.entities[0].actions[0].name == 'test-action'
        assert rep.entities[0].actions.__len__() == 1
        assert rep.classes == ['NewRepresentationCollection']







