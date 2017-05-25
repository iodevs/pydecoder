# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, redefined-outer-name

from pyresult import is_error

from pydecoder.primitives import to_string


def test_to_string_return_error_if_value_is_none():
    rv = to_string(None)

    assert is_error(rv)
