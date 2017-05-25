# -*- coding: utf-8 -*-
'''Decoder structures'''

from toolz import curry


@curry
def array(factory, vals):
    '''Decode string/value as list'''
    return [factory(val) for val in vals]
