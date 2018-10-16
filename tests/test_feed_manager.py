from .context import newsparser

import unittest

dir(newsparser)

class FeedManagerTestSuite(unittest.TestCase):

    def test_add_feed_remove_feed(self):
        feed_manager = newsparser.FeedManager()
        feed_manager.create_tables_if_absent()
        feed_manager.add_feed("www.test1.html","test1")
        feed_manager.add_feed("www.test2.html","test2")
        feeds = feed_manager.get_feeds()
        self.assertEqual(2,len(feeds))
        feed_manager.remove_feed("www.test1.html")
        feed_manager.remove_feed("www.test2.html")
        feeds = feed_manager.get_feeds()
        self.assertEqual(0,len(feeds))

if __name__ == '__main__':
    unittest.main()
