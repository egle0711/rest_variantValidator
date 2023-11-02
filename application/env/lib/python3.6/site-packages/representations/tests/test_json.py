import json

from representations.bin.link import Link


def test_dump_all_required():
    """
    It is possible to dump a link containing only REQUIRED attributes.
    Dump result is consistent in types and values.
    :return:
    """
    l = Link.create(
        href='http://google.com',
        rel='google'
    )
    text = l.dump()

    loaded = json.loads(text)
    assert loaded
    assert len(loaded.keys()) == 2
    assert [k for k, v in loaded.items() if (k, v) in (('href', 'http://google.com'), ('rel', 'google'))]
    assert isinstance(text, str)
    assert l.obj_name == 'links'


def test_load():
    link = Link.create().load('{"href": "http://google.com", "rel": ["self", "search"]}')
    assert link
