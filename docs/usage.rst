=====
Usage
=====

Using PyDecoder in a project to decode JSON data.

.. code-block:: python

    >>> from pydecoder.fields import required, optional, hardcoded
    >>> from pydecoder.json import to_int, to_string, to_bool, decode

    # We have loaded JSON data to dict
    >>> data = {
    ...     'name': 'Jozin Zbazin',
    ...     'age': 42,
    ...     'is_admin': True
    ... }

    # Now describe data validators/decoders
    >>> decoders = [
    ...     required('name', to_string),
    ...     required('age', to_int),
    ...     optional('is_admin', to_bool, False),
    ...     hardcoded(True)
    ... ]

    # User object
    >>> class User(object):
    ...     def __init__(self, name, age, is_admin, is_hero):
    ...         self.name = name
    ...         self.age = age
    ...         self.is_admin = is_admin
    ...         self.is_hero = is_hero

    # And now decode and create user
    >>> rv = decode(lambda data: User(*data), decoders, data)  # return user in result
    >>> rv
    Result(status='Ok', value=<__main__.User...>)

    >>> user = rv.value
    >>> user.name
    'Jozin Zbazin'
    >>> user.age
    42
    >>> user.is_admin
    True
    >>> user.is_hero
    True


Why use PyDecoder instead of raw JSON data?
-------------------------------------------

If the decoder fails, do not create the final object and returns error mesage

.. code-block:: python

    # We have loaded JSON data to dict
    >>> data = {
    ...     'name': 'Jozin Zbazin',
    ...     'age': 'I do not know',
    ...     'is_admin': True
    ... }

    # And decode wrong data
    >>> decode(lambda data: User(*data), decoders, data)  # return user in result
    Result(status='Error', value=[None, "Field 'age' has error: invalid literal for int() with base 10: 'I do not know'", None, None])

or use default data

.. code-block:: python

    # We have loaded JSON data to dict
    >>> data = {
    ...     'name': 'Jozin Zbazin',
    ...     'age': 42,
    ...     'is_admin': "Yes, I'm"
    ... }

    # And decode wrong data
    >>> rv = decode(lambda data: User(*data), decoders, data)  # return user in result
    >>> rv
    Result(status='Ok', value=<__main__.User...>)

    >>> user = rv.value
    >>> user.name
    'Jozin Zbazin'
    >>> user.age
    42
    >>> user.is_admin  # default value
    False
    >>> user.is_hero
    True
