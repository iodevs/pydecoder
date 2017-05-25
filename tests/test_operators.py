# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

from pyresult import ok, is_ok, value, error, is_error

from pydecoder.operators import pipe, dmap, and_then
from pydecoder.primitives import to_int


def test_pipe_pass_value_trough_pipeline():
    def inc(val):
        return ok(val + 1)

    rv = pipe(
        [
            inc,
            inc,
            inc,
        ],
        1
    )

    assert is_ok(rv)
    assert value(rv) == 4


def test_dmap_apply_function_to_decoded_val():
    rv = dmap(lambda x: x + 1, to_int, '1')

    assert is_ok(rv)
    assert value(rv) == 2


def test_and_then_run_next_decoder():
    def dec(val):
        return ok(val - 1)

    rv = and_then(
        dec,
        to_int,
        5
    )

    assert is_ok(rv)
    assert value(rv) == 4


def test_and_then_dont_run_next_decoder():
    def dec(_val):
        return error('ERROR')

    rv = and_then(
        dec,
        to_int,
        5
    )

    assert is_error(rv)
    assert rv.value == 'ERROR'
