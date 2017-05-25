# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, redefined-outer-name, no-value-for-parameter

from pyresult import is_ok, value
from six.moves import zip

from pydecoder.primitives import to_int
from pydecoder.structs import array


def test_array_returns_decoded_result_list():
    ins = ['1', '2', '3']

    rv = array(to_int, ins)

    for orig, res in zip(ins, rv):
        assert is_ok(res)
        assert value(res) == int(orig)
