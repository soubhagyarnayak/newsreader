import logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
import json
import pika


from hacker_news_manager import HackerNewsManager
from oped_manager import OpEdManager
from archiver import Archiver
from config import QUEUE_CONNECTION_STRING
from pika_consumer import PikaConsumer

TASK_PROCESSOR_QUEUE_NAME = 'newsparser'

logger = logging.getLogger(__name__)

def _handler(body):
        try:
            body = body.decode('utf8').replace("'", '"')
            logger.info('Processing message:'+body)
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
                archiver.archive_webpage(message['url'],message['id'])
            elif message['command'] == 'purgeHN':
                logger.info('Purging old hn entries')
                hn = HackerNewsManager()
                hn.purge()
            else:
                logger.error("Command:{} is not supported".format(message.command))
            logger.info('Processing completed successfully.')
        except Exception:
            logger.exception('Processing completed with exception.')
        

class TaskProcessor():
    def __init__(self):
        self.create_listener()

    def start(self):
        logger.info('Listening for messages')
        while True:
            try:
                self.listener.run()
            except KeyboardInterrupt:
                self.listener.stop()
                break

    def create_listener(self):
        self.listener = PikaConsumer(_handler)

try:
    tp = TaskProcessor()
    tp.start()
except Exception as e:
    logger.exception('Encountered unhandled exception.')
