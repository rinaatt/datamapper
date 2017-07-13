import unittest
from ..pipelines import RssFeedPipeline


class TestRssFeedPipeline(unittest.TestCase):
    db_place = ':memory:'

    def setUp(self):
        """
        Setup a temporary database
        """
        self.pipeline = RssFeedPipeline(self.db_place)

    def test_process_one(self):
        result = 2 + 2
        self.assertEqual(result, 4)

    def test_second(self):
        result = 2 * 2
        self.assertEqual(result, 4)


if __name__ == '__main__':
    unittest.main()
