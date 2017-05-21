# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, import-error, redefined-outer-name

import pytest

from toolz import curry, get_in

from pydecoder.fields import hardcoded, optional, required

from pyresult import is_ok, is_error, value, ok, error


@curry
def getter(data, key):
    val = get_in([key], data)
    if val is None:
        return error('Value does not exist.')

    return ok(val)

# def ok_factory(val):
#     return ok(val)


@pytest.fixture
def data():
    return {
        'x': 123,
        's': 'foo bar baz'
    }


def test_required_return_ok_result(data):
    rv = required('x', ok, getter(data))  # pylint: disable=no-value-for-parameter

    assert is_ok(rv)
    assert value(rv) == 123


def test_required_return_error(data):
    rv = required('x', error, getter(data))  # pylint: disable=no-value-for-parameter

    assert is_error(rv)


def test_hardcoded_return_ok_result():
    rv = hardcoded(2.5, None)

    assert is_ok(rv)
    assert value(rv) == 2.5


def test_optional_return_decoded_value_in_result(data):
    rv = optional('x', ok, 'foo', getter(data))  # pylint: disable=no-value-for-parameter

    assert is_ok(rv)
    assert value(rv) == 123


def test_optional_return_default_value_in_result(data):
    rv = optional('y', error, 'foo', getter(data))  # pylint: disable=no-value-for-parameter

    assert is_ok(rv)
    assert value(rv) == 'foo'


def test_optional_return_default_value_in_result_if_value_isnt_found(data):
    rv = optional('y', ok, 'foo', getter(data))  # pylint: disable=no-value-for-parameter

    assert is_ok(rv)
    assert value(rv) == 'foo'
