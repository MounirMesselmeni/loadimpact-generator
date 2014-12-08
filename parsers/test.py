from __future__ import unicode_literals
from __future__ import absolute_import

import unittest

from jmeter_parser import JMeterParser


class JMeterParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        parser = JMeterParser()
        cls.data = parser.get_data()

    def test_testname(self):
        self.assertEqual(self.data['testname'], 'My test plan')

    def test_num_threads(self):
        self.assertEqual(int(self.data['num_threads']), 50)

    def test_ramp_time(self):
        self.assertEqual(int(self.data['ramp_time']), 60)

    def test_domain(self):
        self.assertEqual(self.data['domain'], 'test.loadimpact.com')

    def test_concurrent_pool(self):
        self.assertEqual(int(self.data['concurrent_pool']), 4)

    def test_urls_count(self):
        self.assertEqual(len(self.data['urls']), 5)


if __name__ == '__main__':
    unittest.main()
