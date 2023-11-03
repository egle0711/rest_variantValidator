import pytest

from representations.bin.action import Field, Action
from representations.bin.link import Link
from representations.libs.exceptions import SirenDumpException


class TestField:

    def test_requred(self):
        f = Field.create()
        assert f.obj_name == 'fields'
        assert f
        assert len(f.check_input({}))
        assert f.check_input({})[2] is True
        with pytest.raises(SirenDumpException):
            f.dump()

    def test_dump_with_required(self):
        f = Field.create(name='send-hook')
        assert f
        assert f.dump(indent=4)

    def test_type_positive(self):
        for t in Field.TYPES:
            f = Field.create(name='send-hook', type=t)
            assert f
            assert f.dump()
            assert 'type' in f.keys()
            assert 'name' in f.keys()
            assert f.__len__() == 2

    def test_type_negative(self):
        with pytest.raises(TypeError):
            Field.create(name='send-hook', type='someype')

    def test_all_fields(self):
        f = Field.create(**{
            'class': 'Search',
            'type': 'search',
            'value': 'some text',
            'title': 'some title',
            'name': 'search-criterion'
        })
        f.append({'class': 'Test'})
        assert f
        assert f.dump(indent=4)
        assert f.obj_name == 'fields'
        assert f.name == 'search-criterion'
        assert f.title == 'some title'
        assert f.value == 'some text'
        assert f.classes == ['Search', 'Test']
        assert f.type == 'search'

    def test_all_fields_and_one_more(self):
        f = Field.create(**{
            'class': 'Search',
            'type': 'search',
            'value': 'some text',
            'title': 'some title',
            'name': 'search-criterion'
        })
        f.append(Link.create(href='https://google.com', rel='google'))
        assert f.links
        assert f.links.dump()
        with pytest.raises(SirenDumpException):
            f.dump()


class TestAction:

    def test_requried_negative(self):
        ac = Action.create()
        with pytest.raises(SirenDumpException):
            ac.dump(indent=6)

    def test_requred_positive(self):
        ac = Action.create(
            name='do-search',
            href='http://localhost:3000/search'
        )
        assert ac
        assert ac.name == 'do-search'
        assert ac.type == 'application/x-www-form-urlencoded'
        assert ac.href == 'http://localhost:3000/search'
        assert ac.obj_name == 'actions'
        assert ac.dump()

    def test_required_with_fields(self):
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

        assert ac
        assert ac.name == 'do-search'
        assert ac.type == 'application/x-www-form-urlencoded'
        assert ac.href == 'http://localhost:3000/search'
        assert ac.obj_name == 'actions'
        assert ac.dump()
        assert isinstance(ac.fields, list)
        assert len(ac.fields) == 2
        assert sum([True for i in ac.fields if i.name == 'input']) == len(ac.fields)








