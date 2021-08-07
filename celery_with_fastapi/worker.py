# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                      define the celery app and config.
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

import os
from celery import Celery
os.environ['BROKER_URI'] = 'pyamqp://'
os.environ['BACKEND_URI'] = 'rpc://'


BROKER_URI = os.environ['BROKER_URI']
BACKEND_URI = os.environ['BACKEND_URI']

app = Celery(
    'celery_app',
    broker=BROKER_URI,
    backend=BACKEND_URI,
    include=['tasks']
)

# delete previously stuck tasks in the queue.
# if this command is not used, celery workers will resume tasks stuck in the queue even if computer restarts
app.control.purge()
