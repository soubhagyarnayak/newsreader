import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_CONFIG = {
    'type': os.environ['DB_TYPE'],
    'host': os.environ['DB_HOST'],
    'dbname': os.environ['DB_NAME'],
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
}
QUEUE_CONNECTION_STRING = os.environ['QUEUE_CONNECTION_STRING']
