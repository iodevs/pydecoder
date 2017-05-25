# -*- coding: utf-8 -*-
'''Library fo json decode'''

from pyresult import (
    ok,
    error,
    rmap,
    fold
)
from toolz import curry, get_in

from pydecoder.primitives import (  # noqa pylint: disable=unused-import
    to_int,
    to_float,
    to_string,
    to_bool,
    null,
)


def _to_key_list(keys):
    if not isinstance(keys, tuple) and not isinstance(keys, list):
        return (keys, )
    return keys


@curry
def getter(json, keys):  # pylint: disable=redefined-outer-name
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
def decode(creator, decoders, json_data):
    '''Run decoders on json and result pass to creator function

    json: (args -> value) -> List Decoder -> Json -> Result err value
    '''
    values = [decoder(getter(json_data)) for decoder in decoders]  # pylint: disable=no-value-for-parameter

    return rmap(creator, fold(values))
