import logging

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')  # noqa
import json

from custom_fetcher import SambadaFetcher, TesseractTextExtractor
from hacker_news_manager import HackerNewsManager
from oped_manager import OpEdManager
from archiver import Archiver
from pika_consumer import PikaConsumer
from feed_fetcher import FeedparserRssFetcher
from rss_metadata_store import RSSMetadataStore
from rss_feed_store import RSSFeedStore

TASK_PROCESSOR_QUEUE_NAME = 'newsparser'

logger = logging.getLogger(__name__)


def _handler(body):
    try:
        body = body.decode('utf8').replace("'", '"')
        logger.info(f'Processing message:{body}')
        message = json.loads(body)
        if message['command'] == 'processHN':
            logger.info('Processing HN')
            hn = HackerNewsManager()
            hn.process()
        elif message['command'] == 'processOpEd':
            logger.info('Processing OpEd')
            oped_manager = OpEdManager()
            oped_manager.process()
        elif message['command'] == 'archive':
            logger.info('Archiving content')
            archiver = Archiver()
            archiver.archive_webpage(message['url'], message['id'])
        elif message['command'] == 'purgeHN':
            logger.info('Purging old hn entries')
            hn = HackerNewsManager()
            hn.purge()
        elif message['command'] == 'fetchNews':
            logger.info(f"Fetching news for newspaper: {message['newspaper']}")
            newspaper = message['newspaper']
            if newspaper == 'sambada':
                sambda_fetcher = SambadaFetcher()
                sambda_fetcher.process(message['date'], extractor=TesseractTextExtractor())
            else:
                logger.error(f"Newspaper:{newspaper} is not supported")

        elif message['command'] == 'refreshRSS':
            feed_id = message['feedId']
            logger.info(f"Refreshing RSS entries for feed_id:{feed_id}")
            metadata_store = RSSMetadataStore()
            feed = metadata_store.get_feed_by_id(feed_id)
            if feed is None:
                logger.error(f"No RSS feed found for feed_id:{feed_id}")
            else:
                entries = FeedparserRssFetcher().get_feeds(feed.url)
                RSSFeedStore().add_entries(feed_id, entries)
                metadata_store.update_last_updated(feed_id)
                logger.info(f"Refreshed {len(entries)} entries for feed_id:{feed_id}")
        else:
            logger.error(f"Command:{message['command']} is not supported")
        logger.info('Processing completed successfully.')
    except Exception:
        logger.exception('Processing completed with exception.')


class TaskProcessor:
    def __init__(self):
        self.listener = PikaConsumer(_handler)

    def start(self):
        logger.info('Listening for messages')
        while True:
            try:
                self.listener.run()
            except KeyboardInterrupt:
                self.listener.stop()
                break


try:
    tp = TaskProcessor()
    tp.start()
except Exception:
    logger.exception('Encountered unhandled exception.')
