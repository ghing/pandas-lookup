import io
import os

import pandas as pd
import requests
import six
import yaml


def _make_path(keys, value, ext, version=None):
    """Generate a path to a lookup table or metadata"""
    if isinstance(keys, (list, tuple)):
        keys = '/'.join(keys)

    version_str = ''
    if version:
        version_str = '.{0}'.format(version)

    path = '{keys}/{value}{version}{ext}'.format(
            keys=keys,
            value=value,
            version=version_str,
            ext=ext
    )

    return path


def make_table_path(keys, value, version=None):
    """
    Generate a path to find a given lookup table.
    """
    return _make_path(keys, value, '.csv', version)


def make_metadata_path(keys, value, version=None):
    """
    Generate a path to find a given lookup table.
    """
    return _make_path(keys, value, '.csv.yml', version)


def type_to_converter(type_name):
    type_map = {
        'Text': str,
        'Number': pd.to_numeric
    }

    return type_map[type_name]


def make_converters(meta):
    """
    Uses parsed lookup table metadata to create a dictionary that will use the
    specified types for the table columns (and avoid the overhead of type
    inference).
    """
    converters = {}

    for k, v in meta['columns'].items():
        converters[k] = type_to_converter(v['type'])

    return converters


class Source(object):
    """
    A reference to an archive of lookup tables. This is a remote location with
    lookup table and metadata files at a known path structure.
    :param root:
        The root URL to prefix all data and metadata paths.
    :param cache:
        A path in which to store cached copies of any tables that are used, so
        they can continue to be used offline.
    """
    def __init__(self, root='http://wireservice.github.io/lookup',
                 cache='~/.lookup'):
        self._root = root
        self._cache = os.path.expanduser(cache) if cache else None

    def _read_cache(self, path):
        """
        Read a file from the lookup cache.
        """
        if self._cache:
            cache_path = os.path.join(self._cache, path)

            if os.path.exists(cache_path):
                with io.open(cache_path, encoding='utf-8') as f:
                    text = f.read()

                return text

        msg = ('Unable to download remote file "{0}" and local cache is not '
               'available.').format(path)
        raise RuntimeError(msg)

    def _write_cache(self, path, text):
        """
        Write a file to the lookup cache.
        """
        if self._cache:
            cache_path = os.path.join(self._cache, path)

            folder = os.path.split(cache_path)[0]

            if not os.path.exists(folder):
                os.makedirs(folder)

            with io.open(cache_path, 'w', encoding='utf-8') as f:
                f.write(text)

    def get_metadata(self, keys, value, version=None):
        """
        Fetches metadata related to a specific lookup table.
        See :meth:`Source.get_table` for parameter details.
        """
        path = make_metadata_path(keys, value, version)
        url = '{root}/{path}'.format(root=self._root, path=path)

        try:
            r = requests.get(url)
            text = r.text

            self._write_cache(path, text)
        except (requests.ConnectionError, requests.Timeout):
            text = self._read_cache(path)

        try:
            data = yaml.load(text)
        except yaml.YAMLError:
            raise ValueError('Failed to read or parse YAML at %s' % url)

        return data

    def get_table(self, keys, value, version=None):
        """
        Fetches and creates and agate table from a specified lookup table.
        The resulting table will automatically have row names created for the
        key columns, thus allowing it to be used as a lookup.
        :param keys:
            Either a single string or a sequence of keys that identify the
            "left side" of the table. For example :code:`'fips'` or
            :code:`['city', 'year']`.
        :param value:
            The value that is being looked up from the given keys. For example
            :code:`'state'` or :code:`'population'`.
        :param version:
            An optional version of the given lookup, if more than one exists.
            For instance :code:`'2007'` for the 2007 edition of the NAICS codes
            or :code:`'2012'` for the 2012 version.
        """
        meta = self.get_metadata(keys, value, version)

        path = make_table_path(keys, value, version)
        url = '{root}/{path}'.format(root=self._root, path=path)

        try:
            r = requests.get(url)
            text = r.text

            self._write_cache(path, text)

        except (requests.ConnectionError, requests.Timeout):
            text = self._read_cache(path)

        converters = make_converters(meta)
        return pd.read_csv(six.StringIO(text), converters=converters)
