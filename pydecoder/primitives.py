# -*- coding: utf-8 -*-
'''Decode primitives'''

from pyresult import (
    ok,
    error
)
from six import u, string_types, text_type


def to_int(val):
    '''Decode string/value to int'''
    try:
        return ok(int(val))
    except (TypeError, ValueError) as err:
        return error(text_type(err))


def to_float(val):
    '''Decode string/value to float'''
    try:
        return ok(float(val))
    except (TypeError, ValueError) as err:
        return error(text_type(err))


def to_string(val):
    '''Decode string/value to string'''
    if val is None:
        return error(u'Can\'t be null')

    return ok(val) if isinstance(val, text_type) else ok(text_type(val, 'utf-8'))


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


def null(val):
    '''Decode string/value to None'''
    if val is not None and val.lower() not in ('none', 'null'):
        return error(u('Value can\'t be decoded'))
    return ok(None)
