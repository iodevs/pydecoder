# -*- coding: utf-8 -*-
'''Decoder structures'''

from pyresult import is_error, value, ok, error
from six import u
from toolz import curry


@curry
def array(factory, vals):
    '''Decode string/value as list

    array :: (a -> Result e b) -> List a -> Result e (List b)

    >>> from pydecoder.primitives import to_int
    >>> array(to_int, [1, 2, 3])
    Result(status='Ok', value=[1, 2, 3])

    >>> array(to_int, None)
    Result(status='Error', value="'None' isn't list or tuple.")
    '''
    if not isinstance(vals, (list, tuple)):
        return error(u('\'{}\' isn\'t list or tuple.').format(vals))

    result = []

    for val in vals:
        rv = factory(val)

        if is_error(rv):
            return rv

        result.append(value(rv))

    return ok(result)
