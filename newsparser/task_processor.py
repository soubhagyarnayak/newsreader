import json
import pika

from hacker_news_manager import HackerNewsManager
from oped_manager import OpEdManager

TASK_PROCESSOR_QUEUE_NAME = 'newsparser'

def _handler(channel,method,properties,body):
        try:
            body = body.decode('utf8').replace("'", '"')
            print('Processing message:'+body)
            message = json.loads(body)
            if message['command'] == 'processHN':
                print('Processing HN')
                hn = HackerNewsManager()
                hn.process()
            elif message['command'] == 'processOpEd':
                print('Processing OpEd')
                oped_manager = OpEdManager()
                oped_manager.process()
            else:
                print("Command:{} is not supported".format(message.command))
            print('Processing completed successfully.')
        except Exception as e:
            print(e)
            print('Processing completed with exception.')
        

class TaskProcessor():
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=TASK_PROCESSOR_QUEUE_NAME)
        self.channel.basic_consume(_handler,queue=TASK_PROCESSOR_QUEUE_NAME,no_ack=True)

    def start(self):
        print('Listening for messages')
        self.channel.start_consuming()

tp = TaskProcessor()
tp.start()