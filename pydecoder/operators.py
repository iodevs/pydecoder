# -*- coding: utf-8 -*-
'''Decoder operators'''

from pyresult import (
    ok,
    rmap,
    and_then as andthen
)
from six.moves import reduce
from toolz import curry


@curry
def and_then(next_decoder, decoder, val):
    '''Run `next_decoder` after `decoder` success run with `val`

    and_then: (a -> Result b) -> (val -> Result a) -> val -> Result b
    '''
    return andthen(next_decoder, decoder(val))


@curry
def dmap(func, decoder, val):
    '''Run `decoder` with `val` and then map `func` to result

    dmap: (a -> value) -> (val -> Result a) -> val -> Result value
    '''
    return rmap(func, decoder(val))


@curry
def pipe(funcs, val):
    '''Pass value trough funcs

    pipe: List (value -> Result a) -> value -> Result a
    '''
    return reduce(lambda acc, item: andthen(item, acc), funcs, ok(val))
