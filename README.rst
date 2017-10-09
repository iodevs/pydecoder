=========
PyDecoder
=========


.. image:: https://img.shields.io/pypi/v/pydecoder.svg
        :target: https://pypi.python.org/pypi/pydecoder

.. image:: https://img.shields.io/travis/iodevs/pydecoder.svg
        :target: https://travis-ci.org/iodevs/pydecoder

.. image:: https://readthedocs.org/projects/pydecoder/badge/?version=latest
        :target: https://pydecoder.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/iodevs/pydecoder/shield.svg
        :target: https://pyup.io/repos/github/iodevs/pydecoder/
        :alt: Updates

.. image:: https://coveralls.io/repos/github/iodevs/pydecoder/badge.svg?branch=master
        :target: https://coveralls.io/github/iodevs/pydecoder?branch=master


A XML, JSON,... decode library


* Free software: BSD license
* Documentation: https://pydecoder.readthedocs.io.


Features
--------

* Decode and validate values from XML and JSON.

Install
-------

To install PyDecoder, run this command in your terminal:

.. code-block:: console

    $ pip install pydecoder


Example
-------

.. code:: python

    >>> from pydecoder.fields import required, optional
    >>> from pydecoder.json import to_int, to_string, decode

    # Define data
    >>> data = {'foo': 'Text', 'bar': 1}

    # Describe data
    >>> decoders = [
    ...     required('foo', to_string),
    ...     required('bar', to_int),
    ...     optional('baz', to_int, -5),
    ... ]

    # Decode/verify data
    >>> decode(lambda x: x, decoders, data)
    Result(status='Ok', value=['Text', 1, -5])


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

