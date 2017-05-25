# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

from collections import Iterator

from six import wraps, u
from six.moves import map

from toolz import curry, first

from pyresult import (
    ok,
    error,
    rmap,
    fold,
)

from pydecoder.primitives import (
    to_int,
    to_float,
    to_string,
    to_bool,
    null,
)


def to_val(func):
    '''Convert iterator to value'''
    @wraps(func)
    def _to_val(iterator_or_value):
        if isinstance(iterator_or_value, Iterator):
            try:
                return func(first(iterator_or_value))
            except StopIteration:
                return error(u('Value is empty.'))
        return func(iterator_or_value)

    return _to_val


@curry
def getter(tree, key):
    '''Get data from tree'''
    return ok(map(lambda elm: elm.text, tree.iterfind(key)))


@curry
def decode(creator, decoders, tree):
    '''Run decoders on xml and result pass to creator function

    xml: (args -> value) -> List Decoder -> ElementTree -> Result value err
    '''
    values = [decoder(getter(tree)) for decoder in decoders]  # pylint: disable=no-value-for-parameter

    return rmap(creator, fold(values))


to_int = to_val(to_int)  # pylint: disable=invalid-name
to_float = to_val(to_float)  # pylint: disable=invalid-name
to_string = to_val(to_string)  # pylint: disable=invalid-name
to_bool = to_val(to_bool)  # pylint: disable=invalid-name
null = to_val(null)  # pylint: disable=invalid-name
