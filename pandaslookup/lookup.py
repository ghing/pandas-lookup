import pandas as pd

from .source import Source


DEFAULT_SOURCE = Source()


def lookup(df, key, value, lookup_key=None, version=None, source=None):
    """
    Fetch a lookup table from the remote source, matches it with this
    `DataFrame` by its key columns, appends the value column and returns a new
    `DataFrame`.

    :param df:
        `pandas.DataFrame` into which the lookup table will be merged.
    :param key:
        A column name or a sequence of such names to match in this table.
    :param value:
        The value that is being looked up. For example :code:`'description'`
        or :code:`'population'`. This is the column that will be appended.
    :param lookup_key:
        A column name or a sequence of such names to match in the lookup
        table. For example :code:`'naics'` or :code:`['city', 'year']`.
        This defaults the same values specified for `key`, so it
        only needs to be specified if the column names in this table
        aren't the same.
    :param version:
        An optional version of the lookup to use, if more than one exists.
        For instance :code:`'2007'` for the 2007 edition of the NAICS codes
        or :code:`'2012'` for the 2012 version.
    :param source:
        An instance of :class:`.Source` that defines where lookup tables
        are located. If not specified a default source will be used that
        points to the
        `wireservice/lookup <https://github.com/wireservice/lookup>`_
        repository.
    """
    if source is None:
        source = DEFAULT_SOURCE

    table = source.get_table(lookup_key or key, value, version)

    result = pd.merge(
        df,
        table,
        how='left',
        left_on=key,
        right_on=lookup_key or key
    )

    if lookup_key:
        result = result.drop(key, axis=1)

    return result


def from_lookup(lookup_key, value, version=None, source=None):
    """
    Fetch a lookup table, but don't join it to anything. See
    `lookup` for arguments.
    """
    if source is None:
        source = DEFAULT_SOURCE

    return source.get_table(lookup_key, value, version)
