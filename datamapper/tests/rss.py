import os
import sqlite3
import unittest
import logging


class TestRssFeed(unittest.TestCase):
    db_place = ':memory:'

    def setUp(self):
        """
        Setup a temporary database
        """
        conn = sqlite3.connect(self.db_place)
        cursor = conn.cursor()
        # create a table
        cursor.execute(
            "CREATE TABLE rss_news ("
            " id PRIMARY KEY,"
            " title TEXT,"
            " link TEXT,"
            " guid TEXT,"
            " pub_date TEXT,"
            " description TEXT"
            ")"
        )
        # save to database
        conn.commit()

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
