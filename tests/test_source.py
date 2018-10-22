import unittest

from pandaslookup.source import Source


class TestSource(unittest.TestCase):
    def setUp(self):
        self.source = Source()

    def test_get_metadata(self):
        meta = self.source.get_metadata('usps', 'state')

        self.assertIn('Census Bureau', meta['sources'][0])

    def test_get_table(self):
        table = self.source.get_table('usps', 'state')

        self.assertEqual(list(table.columns), ['usps', 'state'])
        self.assertEqual(table.iloc[0]['usps'], 'AL')
        self.assertEqual(table.iloc[1]['usps'], 'AK')

    def test_get_table_multiple_keys(self):
        table = self.source.get_table(['year', 'month'], 'cpi.sa')

        self.assertEqual(list(table.columns), ['year', 'month', 'cpi'])
        self.assertEqual(table.iloc[0]['year'], '1947')
        self.assertEqual(table.iloc[0]['month'], '1')
        self.assertEqual(table.iloc[1]['year'], '1947')
        self.assertEqual(table.iloc[1]['month'], '2')
