# -*- coding: utf-8 -*-
'''Library fo json decode'''

from pyresult import (
    ok,
    error,
    rmap,
    fold,
    # and_then as andthen  # pylint: disable=import-error
)
from toolz import curry, get_in


def _to_key_list(keys):
    if not isinstance(keys, tuple) and not isinstance(keys, list):
        return (keys, )
    return keys


@curry
def getter(json, keys):
    '''Get data from json'''

    try:
        return ok(
            get_in(
                _to_key_list(keys),
                json,
                no_default=True
            )
        )
    except KeyError:
        return error(u'Value is empty or path/key {0!r} not found...'.format(keys))


@curry
def json(creator, decoders, json_data):
    '''Run decoders on json and result pass to creator function

    json: (args -> value) -> List Decoder -> Json -> Result err value
    '''
    values = [decoder(getter(json_data)) for decoder in decoders]  # pylint: disable=no-value-for-parameter

    return rmap(creator, fold(values))
