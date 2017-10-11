# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
'''
A fields descriptors.
'''

from toolz import curry

from pyresult.result import ok, is_ok
from pyresult.operators import and_then, errmap


@curry
def _errmgs(key, msg):
    return u'Field \'%s\' has error: %s' % (key, msg)


@curry
def field(key, factory, getter):
    '''Field decoder

    field ::
        (Tuple String | String)
        -> (a -> Result e b)
        -> (data -> (Tuple String | String) -> Result e a)
        -> Result e b
    '''
    return errmap(
        _errmgs(key),  # pylint: disable=no-value-for-parameter
        and_then(factory, getter(key))
    )


@curry
def required(key, factory, getter):
    '''Mark field as required

    required ::
        (Tuple String | String)
        -> (a -> Result e b)
        -> (data -> (Tuple String | String) -> Result e a)
        -> Result e b

    >>> from pydecoder.fields import required
    >>> from pydecoder.json import getter, to_string

    Required fields is in data

    >>> required('foo', to_string, getter({'foo': 'bar'}))
    Result(status='Ok', value='bar')

    Retrun error if data not found

    >>> required('fiz', to_string, getter({'foo': 'bar'}))
    Result(status='Error', value="Field 'fiz' has error: Value is empty or path/key 'fiz' not found...")

    or data is invalid

    >>> required('foo', to_string, getter({'foo': 1234}))
    Result(status='Error', value="Field 'foo' has error: '1234' isn't string.")
    '''
    return field(key, factory, getter)


@curry
def optional(key, factory, default, getter):
    '''Mark field as optional

    optional ::
        (Tuple String | String)
        -> (a -> Result e b)
        -> b
        -> (data -> (Tuple String | String) -> Result e a)
        -> Result e b

    >>> from pydecoder.fields import optional
    >>> from pydecoder.json import getter, to_string

    Returns value if key is found

    >>> optional('foo', to_string, 'default', getter({'foo': 'bar'}))
    Result(status='Ok', value='bar')

    or defualt if not found

    >>> optional('fiz', to_string, 'default', getter({'foo': 'bar'}))
    Result(status='Ok', value='default')

    or an error occurs in the decoder

    >>> optional('foo', to_string, 'default', getter({'foo': 1234}))
    Result(status='Ok', value='default')
    '''
    val = field(key, factory, getter)
    return val if is_ok(val) else ok(default)


@curry
def hardcoded(val, _):
    '''Return value as ok result

    hardcoded :: a -> (data -> (Tuple String | String) -> Result e b) -> Result e a

    >>> from pydecoder.fields import hardcoded
    >>> from pydecoder.json import getter

    Returns the specified value

    >>> hardcoded('foo', getter({'bar': 'baz'}))
    Result(status='Ok', value='foo')

    '''
    return ok(val)
