import unittest
try:
    import unittest.mock as mock

except ImportError:
    import mock

import pandas as pd
import requests

from pandaslookup.lookup import from_lookup, lookup
from pandaslookup.source import Source


class TestLookup(unittest.TestCase):
    def setUp(self):
        self._source = Source(cache=False)

    def test_lookup(self):
        rows = [
            ('WA',),
            ('VA',),
            ('TX',)
        ]

        column_names = ['usps']

        table = pd.DataFrame.from_records(rows, columns=column_names)

        result = lookup(table, 'usps', 'state', source=self._source)

        self.assertEqual(list(result.columns), ['usps', 'state'])

        self.assertEqual(result.iloc[1].tolist(), ['VA', 'Virginia'])

    def test_lookup_key(self):
        rows = [
            ('WA',),
            ('VA',),
            ('TX',)
        ]

        column_names = ['postal']

        table = pd.DataFrame.from_records(rows, columns=column_names)

        result = lookup(table, 'postal', 'state', lookup_key='usps',
                        source=self._source)

        self.assertEqual(list(result.columns), ['usps', 'state'])

        self.assertEqual(result.iloc[1].tolist(), ['VA', 'Virginia'])

    def test_lookup_version(self):
        rows = [
            ('1111',),
            ('313320',),
            ('522310',)
        ]

        column_names = ['naics']

        table = pd.DataFrame.from_records(rows, columns=column_names)

        result = lookup(table, 'naics', 'description', version='2012',
                        source=self._source)

        self.assertEqual(list(result.columns), ['naics', 'description'])

        self.assertEqual(result.iloc[1].tolist(),
                         ['313320', 'Fabric Coating Mills'])

    def test_lookup_multiple_keys(self):
        rows = [
            ('AZ', '1985'),
            ('WY', '2014'),
            ('SC', '1994')
        ]

        column_names = ['usps', 'year']

        table = pd.DataFrame.from_records(rows, columns=column_names)

        result = lookup(table, ['usps', 'year'], 'population',
                        source=self._source)

        self.assertEqual(list(result.columns), ['usps', 'year', 'population'])

        self.assertEqual(result.iloc[1].tolist(), ['WY', '2014', 584153])

    def test_from_lookup(self):
        table = from_lookup('usps', 'state')

        self.assertEqual(list(table.columns), ['usps', 'state'])
        self.assertEqual(table.iloc[1].tolist(), ['AK', 'Alaska'])

    def test_connection_fails(self):
        with mock.patch.object(requests, 'get') as mock_method:
            mock_method.side_effect = requests.ConnectionError

            with self.assertRaises(RuntimeError):
                from_lookup('usps', 'state', source=self._source)

    def test_cache(self):
        source = Source(cache='examples')

        with mock.patch.object(requests, 'get') as mock_method:
            mock_method.side_effect = requests.ConnectionError

            table = from_lookup('usps', 'state', source=source)

        self.assertEqual(list(table.columns), ['usps', 'state'])
