import os
import sqlite3
import unittest
from datamapper.spiders import RssFeedSpider
import logging


class TestRssFeed(unittest.TestCase):
    # db_place = ':memory:'

    def setUp(self):
        """
        Setup a temporary database
        """
        self.spider = RssFeedSpider()

    def tearDown(self):
        """
        Delete the database
        """
        if self.db_place != ':memory:':
            os.remove(self.db_place)

    def test_first(self):
        result = 2 + 2
        self.assertEqual(result, 4)

    def test_second(self):
        result = 2 * 2
        self.assertEqual(result, 4)


if __name__ == '__main__':
    unittest.main()
