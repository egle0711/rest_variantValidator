import json
import pytest
from representations.libs.exceptions import SirenDumpException
from representations.bin.link import Link


class TestLinks:

    def test_create_simple(self):
        Link.create()

    def test_dump_simple(self):
        """
        Impossible to dump a link where there are missing required keys attributes.
        :return:
        """
        with pytest.raises(SirenDumpException):
            Link.create().dump()

    def test_create_all_required(self):
        """
        It is possible to create a link containing all REQUIRED attributes.
        :return:
        """
        l = Link.create(
            href='http://google.com',
            rel='google'
        )
        assert len(l.items()) == 2
        assert l.href == 'http://google.com'
        assert isinstance(l.rel, list)
        assert isinstance(l.href, str)
        assert l.obj_name == 'links'

    def test_all_attributes(self):
        """
        It should be possible to create a link with all possible attrs
        :return:
        """
        l = Link.create(
            href='http://google.com',
            rel='google',
            type='search',
            title='Title',
        )
        l.append({'class': 'SearchLink'})
        assert l.items().__len__() == 5
        assert type(l.href) == str and l.href == 'http://google.com'
        assert type(l.rel) == list and l.rel == ['google']
        assert type(l.type) == str and l.type == 'search'
        assert type(l.content['class']) == list and l.content['class'] == ['SearchLink']
        assert type(l.title) == str and l.title == 'Title'
        assert l.obj_name == 'links'

    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            Link()

    def test_dump_extra_args(self):
        google_link = Link.create(
            href='http://google.com',
            rel='google',
            entities=Link.create(
                href='http://localhost:3000',
                rel='self'
            )
        )
        with pytest.raises(SirenDumpException):
            d = google_link._dict
        assert google_link.entities.dump(), 'Should be possible to dump'
        with pytest.raises(SirenDumpException):
            google_link.dump()







