# makes sure celery is imported
from .celery import app as celery_app


__all__ = ("celery_app",)

__version__ = "0.0.1"
