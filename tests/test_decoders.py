# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

import random

import pytest

from pydecoder.xml import (
    to_int,
    to_float,
    to_val,
    to_string,
    to_bool,
    null
)
from pyresult import is_error, is_ok, value


def random_case(string):
    caps = string.upper()
    lowers = string.lower()
    return ''.join(random.choice(x) for x in zip(caps, lowers))


TRUE_VALUES = [True, random_case('True')]
FALSE_VALUES = [False, random_case('False')]


def test_to_int_return_parsed_result():
    rv = to_int('10')

    assert is_ok(rv)
    assert value(rv) == 10


def test_to_int_return_error_result():
    rv = to_int(None)

    assert is_error(rv)


def test_to_float_return_parsed_result():
    rv = to_float('1.5')

    assert is_ok(rv)
    assert value(rv) == 1.5


def test_to_float_return_error_result():
    rv = to_float('aaa')

    assert is_error(rv)


def test_to_val_return_error_result_if_iterator_is_empty():
    @to_val
    def ftest(val):
        return val

    i = iter([])

    rv = ftest(i)

    assert is_error(rv)
    assert rv.value == 'Value is empty.'


def test_to_string_return_decoded_result():
    rv = to_string('foo')

    assert is_ok(rv)
    assert value(rv) == 'foo'


@pytest.mark.parametrize('val', TRUE_VALUES)
def test_to_bool_return_true_in_decoded_result(val):
    rv = to_bool(val)

    assert is_ok(rv)
    assert value(rv)


@pytest.mark.parametrize('val', FALSE_VALUES)
def test_to_bool_return_false_in_decoded_result(val):
    rv = to_bool(val)

    assert is_ok(rv)
    assert not value(rv)


def test_to_bool_return_error_result_if_value_isnt_string_or_bool():
    rv = to_bool(1)

    assert is_error(rv)


def test_to_bool_return_error_result_if_value_isnt_valid_string():
    rv = to_bool('foo')

    assert is_error(rv)


@pytest.mark.parametrize('val', [None, random_case('none'), random_case('null')])
def test_none_return_none_in_decoded_result(val):
    rv = null(val)

    assert is_ok(rv)
    assert value(rv) is None


def test_none_return_error_result():
    rv = null('aaaa')

    assert is_error(rv)
