# -*- coding: utf-8 -*-

from toolz import curry

from pyresult.result import ok, is_ok
from pyresult.operators import and_then, errmap


@curry
def _errmgs(key, msg):
    return u'Field \'%s\' has error: %s' % (key, msg)


@curry
def field(key, factory, getter):
    '''Field decoder
    '''
    return errmap(
        _errmgs(key),  # pylint: disable=no-value-for-parameter
        and_then(factory, getter(key))
    )


@curry
def required(key, factory, getter):
    '''Mark field as required'''
    return field(key, factory, getter)


@curry
def optional(key, factory, default, getter):
    '''Mark field as optional'''
    val = field(key, factory, getter)
    return val if is_ok(val) else ok(default)


@curry
def hardcoded(val, _):
    '''Return value as ok result'''
    return ok(val)
