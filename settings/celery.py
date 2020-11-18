import os
from celery import Celery

from .environment import env

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')

app = Celery('kodiusshop')

# app.conf.update(
#     #  settings for message broker
#     broker_url=env.str("CLOUDAMQP_URL", default=""),
#     broker_pool_limit=1,
#     broker_heartbeat=None,  #  reduces RabbitMQ connections, recommended by CloudAMQP
#     broker_connection_timeout=30,
#     event_queue_expires=60,
#     worker_prefetch_multiplier=1,
#     worker_concurrency=16,
#     worker_enable_remote_control=False,  #  reduces RabbitMQ connections, recommended by CloudAMQP
#     #  settings for result store
#     # result_backend=os.environ['REDIS_URL'],
#     result_backend=env.str("REDIS_URL", ),
#     redis_max_connections=20
# )

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
