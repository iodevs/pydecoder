# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, import-error, redefined-outer-name

from cmath import isnan

from hypothesis import given
from hypothesis.strategies import (
    one_of,
    none,
    integers,
    text,
    booleans,
    floats,
    complex_numbers,
    fixed_dictionaries,
)

from pyresult import is_ok, is_error, value, ok, error

from pydecoder.json import getter
from pydecoder.fields import hardcoded, optional, required


DATA_STRATEGY = fixed_dictionaries({
    'field': one_of(
        none(),
        integers(),
        text(),
        booleans(),
        floats(),
        complex_numbers(),
    ),
})


def equal(left, right):
    if (isinstance(left, (float, complex))
            and isnan(left)
            and isinstance(right, (float, complex))
            and isnan(right)):
        return True

    return left == right


@given(DATA_STRATEGY)
def test_required_return_ok_result(data):
    rv = required('field', ok, getter(data))  # pylint: disable=no-value-for-parameter

    assert is_ok(rv)
    assert equal(value(rv), data['field'])


@given(DATA_STRATEGY)
def test_required_return_error(data):
    rv = required('field', error, getter(data))  # pylint: disable=no-value-for-parameter

    assert is_error(rv)


def test_hardcoded_return_ok_result():
    rv = hardcoded(2.5, None)

    assert is_ok(rv)
    assert value(rv) == 2.5


@given(DATA_STRATEGY)
def test_optional_return_decoded_value_in_result(data):
    rv = optional('field', ok, 'foo', getter(data))  # pylint: disable=no-value-for-parameter

    assert is_ok(rv)
    assert equal(value(rv), data['field'])


@given(DATA_STRATEGY)
def test_optional_return_default_value_in_result(data):
    rv = optional('y', error, 'foo', getter(data))  # pylint: disable=no-value-for-parameter

    assert is_ok(rv)
    assert value(rv) == 'foo'


@given(DATA_STRATEGY)
def test_optional_return_default_value_in_result_if_value_isnt_found(data):
    rv = optional('y', ok, 'foo', getter(data))  # pylint: disable=no-value-for-parameter

    assert is_ok(rv)
    assert value(rv) == 'foo'
