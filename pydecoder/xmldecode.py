# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

from collections import Iterator

from six import wraps, u, string_types, text_type
from six.moves import map, reduce

from toolz import curry, first

from pyresult import (
    ok,
    error,
    rmap,
    fold,
    and_then as andthen  # pylint: disable=import-error
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
def xml(creator, decoders, tree):
    '''Run decoders on xml and result pass to creator function

    xml: (*args -> value) -> List Decoder -> ElementTree -> Result value err
    '''
    values = [decoder(getter(tree)) for decoder in decoders]  # pylint: disable=no-value-for-parameter

    return rmap(creator, fold(values))


@curry
def array(factory, vals):
    '''Decode string/value as list'''
    return [factory(val) for val in vals]


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


@to_val
def to_int(val):
    '''Decode string/value to int'''
    try:
        return ok(int(val))
    except (TypeError, ValueError) as err:
        return error(text_type(err))


@to_val
def to_float(val):
    '''Decode string/value to float'''
    try:
        return ok(float(val))
    except (TypeError, ValueError) as err:
        return error(text_type(err))


@to_val
def to_string(val):
    '''Decode string/value to string'''
    if val is None:
        return error(u'Can\'t be null')

    return ok(val) if isinstance(val, text_type) else ok(text_type(val, 'utf-8'))


@to_val
def to_bool(val):
    '''Decode string/value to boolean'''
    if isinstance(val, string_types):  # pylint: disable=no-else-return
        lowered_string = val.lower()
        if lowered_string == 'true':  # pylint: disable=no-else-return
            return ok(True)
        elif lowered_string == 'false':
            return ok(False)
        else:
            return error(u('String %s is invalid boolean value.' % val))
    elif isinstance(val, bool):
        return ok(val)
    else:
        return error(u('Value can\'t be decoded'))


@to_val
def null(val):
    '''Decode string/value to None'''
    if val is not None and val.lower() not in ('none', 'null'):
        return error(u('Value can\'t be decoded'))
    return ok(None)
