# -*- coding: utf-8 -*-
'''Decoder structures'''

from pyresult import is_error, value, ok
from toolz import curry


@curry
def array(factory, vals):
    '''Decode string/value as list'''
    result = []

    for val in vals:
        rv = factory(val)

        if is_error(rv):
            return rv

        result.append(value(rv))

    return ok(result)
