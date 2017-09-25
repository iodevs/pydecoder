# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, redefined-outer-name, no-value-for-parameter

from pyresult import is_ok, is_error
from six import string_types
from six.moves import zip

from hypothesis import given
from hypothesis.strategies import (
    lists,
    one_of,
    none,
    integers,
    recursive,
    text,
    booleans,
    floats,
    complex_numbers,
    dictionaries
)

from pydecoder.primitives import to_int
from pydecoder.structs import array


NOT_LIST = recursive(
    none() |
    text() |
    booleans() |
    integers() |
    floats() |
    complex_numbers(),
    lambda children: dictionaries(text(), children)
)


@given(lists(integers()))
def test_array_returns_decoded_list_in_result(ins):

    rv = array(to_int, ins)

    assert is_ok(rv)

    for orig, res in zip(ins, rv.value):
        assert res == int(orig)


@given(lists(one_of(integers(), none()), min_size=1).filter(lambda x: None in x))
def test_stop_on_first_error_and_returns_it(ins):
    rv = array(to_int, ins)

    assert is_error(rv)
    assert isinstance(rv.value, string_types)


@given(NOT_LIST)
def test_array_returns_error_if_value_isnt_valid_list(val):
    rv = array(to_int, val)

    assert is_error(rv)
    assert isinstance(rv.value, string_types)
