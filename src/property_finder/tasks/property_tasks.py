import logging
from typing import Any, Dict

from adapter.celery import celery
from property_finder.repositories.django.property import PropertyDjangoRepository

logger = logging.getLogger(__name__)


@celery.task
def update_property_on_postgresql(pk: int, updates: Dict[str, Any]):
    logger.info(f"Task received with pk: {pk}, updates: {updates}")
    repository = PropertyDjangoRepository()
    repository.update(pk=pk, updates=updates)
