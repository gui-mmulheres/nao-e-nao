from celery import Celery
from celery.signals import after_setup_logger
from logger_config import setup_logger

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)


@after_setup_logger.connect
def setup_celery_logger(logger, *args, **kwargs):
    setup_logger()
