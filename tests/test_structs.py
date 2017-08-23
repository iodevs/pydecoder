# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, redefined-outer-name, no-value-for-parameter

from pyresult import is_ok, is_error
from six import string_types
from six.moves import zip

from pydecoder.primitives import to_int
from pydecoder.structs import array


def test_array_returns_decoded_list_in_result():
    ins = ['1', '2', '3']

    rv = array(to_int, ins)

    assert is_ok(rv)

    for orig, res in zip(ins, rv.value):
        assert res == int(orig)


def test_stop_on_first_error_and_returns_it():
    ins = ['1', None, '3']

    rv = array(to_int, ins)

    assert is_error(rv)
    assert isinstance(rv.value, string_types)
