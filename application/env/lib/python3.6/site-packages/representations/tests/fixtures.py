from pytest import fixture

from representations.bin.action import Action, Field
from representations.tests.helpers import Model


@fixture()
def prepare_models(request):
    return Model()


@fixture()
def prepare_action(request):
    ac = Action.create(
        name='do-search',
        href='http://localhost:3000/search',
        method='GET'
    )
    ac.append(
        (
            Field.create(name='input', value=245),
            Field.create(**{'name': 'input', 'type': 'hidden', 'value': 'Default', 'class': ['Search', 'Test']})
        )
    )
    return ac


