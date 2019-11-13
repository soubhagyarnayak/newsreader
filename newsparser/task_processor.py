import json
import logging
import pika

from hacker_news_manager import HackerNewsManager
from oped_manager import OpEdManager
from archiver import Archiver
from config import QUEUE_CONNECTION_STRING

TASK_PROCESSOR_QUEUE_NAME = 'newsparser'

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def _handler(channel,method,properties,body):
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
        except Exception as e:
            print(e)
            logger.exception('Processing completed with exception.')
        

class TaskProcessor():
    def __init__(self):
        parameters = pika.URLParameters(QUEUE_CONNECTION_STRING)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=TASK_PROCESSOR_QUEUE_NAME)
        self.channel.basic_consume(_handler,queue=TASK_PROCESSOR_QUEUE_NAME,no_ack=True)

    def start(self):
        logger.info('Listening for messages')
        self.channel.start_consuming()

try:
    tp = TaskProcessor()
    tp.start()
except Exception as e:
    print(e)
    print(type(e))
