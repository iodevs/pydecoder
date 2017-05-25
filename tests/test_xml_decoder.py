# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, import-error, redefined-outer-name, no-value-for-parameter

from xml.etree import ElementTree as ET

import pytest

from pydecoder.fields import required
from pydecoder.xml import xml, to_string
from pyresult import is_ok, is_error, value


def creator(values):
    return values


@pytest.fixture
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


@pytest.fixture
def tree(xmlstring):
    return ET.fromstring(xmlstring)


def test_xml_return_ok_result(tree):
    rv = xml(
        creator,
        (
            required('c', to_string),
        ),
        tree
    )

    assert is_ok(rv)
    assert value(rv) == ['foo', ]


def test_xml_return_error_result(tree):
    rv = xml(
        creator,
        (
            required('f', to_string),
        ),
        tree
    )

    assert is_error(rv)


def test_xml_return_error_result_with_aggregate_messages(tree):
    rv = xml(
        creator,
        (
            required('f', to_string),
            required('e', to_string),
        ),
        tree
    )

    assert is_error(rv)
    for msg in rv.value:
        assert msg.find(u'Value is empty.') > -1
