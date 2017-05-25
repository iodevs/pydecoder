# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, import-error, redefined-outer-name, no-value-for-parameter

from json import loads
from xml.etree import ElementTree as ET

import pytest

from pydecoder.fields import required
from pydecoder import xml
from pydecoder import json
from pyresult import is_ok, is_error, value


PARAM = pytest.mark.parametrize


def xmlstring():
    return '''
        <b>
            <a>1</a>
            <a>2</a>
            <a>3</a>
            <c>foo</c>
            <d>true</d>
        </b>
    '''


def tree():
    return ET.fromstring(xmlstring())


def jsonstring():
    return '{"a": [1, 2, 3], "c": "foo", "d": true}'


def json_data():
    return loads(jsonstring())


DECODERS_AND_DATA = (
    (xml, tree()),
    (json, json_data()),
)


IDS = (
    'XML',
    'JSON',
)


def creator(values):
    return values


@PARAM('decoder, data', DECODERS_AND_DATA, ids=IDS)
def test_return_ok_result(decoder, data):
    rv = decoder.decode(
        creator,
        (
            required('c', decoder.to_string),
        ),
        data
    )

    assert is_ok(rv)
    assert value(rv) == ['foo', ]


@PARAM('decoder, data', DECODERS_AND_DATA, ids=IDS)
def test_return_error_result(decoder, data):
    rv = decoder.decode(
        creator,
        (
            required('f', decoder.to_string),
        ),
        data
    )

    assert is_error(rv)


@PARAM('decoder, data', DECODERS_AND_DATA, ids=IDS)
def test_return_error_result_with_aggregate_messages(decoder, data):
    rv = decoder.decode(
        creator,
        (
            required('f', decoder.to_string),
            required('e', decoder.to_string),
        ),
        data
    )

    assert is_error(rv)
    for msg in rv.value:
        assert msg.find(u'Value is empty') > -1


def test_json_decode_return_ok_result_by_path():
    rv = json.decode(
        creator,
        (
            required(['a', 2], json.to_int),
        ),
        json_data()
    )

    assert is_ok(rv)
    assert rv.value == [3, ]
