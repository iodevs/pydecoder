# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, redefined-outer-name

from hypothesis import given
from hypothesis.strategies import (
    lists,
    none,
    integers,
    recursive,
    text,
    booleans,
    floats,
    complex_numbers,
    dictionaries
)
from pyresult import is_error, is_ok, value

from pydecoder.primitives import to_string


NOT_STRING = recursive(
    none() |
    booleans() |
    integers() |
    floats() |
    complex_numbers(),
    lambda children: lists(children) | dictionaries(text(), children)
)


@given(NOT_STRING)
def test_to_string_return_error_if_value_isnt_string(val):
    rv = to_string(val)

    assert is_error(rv)


@given(text())
def test_to_string_returns_ok_result(val):
    rv = to_string(val)

    assert is_ok(rv)
    assert value(rv) == val
