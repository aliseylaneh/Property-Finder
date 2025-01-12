from enum import StrEnum
from typing import Any, Dict

from pydantic import BaseModel

from property_finder.models.types.types import RepositoryModelType


class DomainEventTypes(StrEnum):
    # Property events
    PROPERTY_UPDATED = "PROPERTY_UPDATED"
    PROPERTY_DELETED = "PROPERTY_DELETED"

    # Agent events
    AGENT_UPDATED = "AGENT_UPDATED"
    AGENT_DELETED = "AGENT_DELETED"


class BaseEvent(BaseModel):
    repo_name: RepositoryModelType
    event_type: DomainEventTypes


class UpdateEvent(BaseEvent):
    pk: int
    updates: Dict[str, Any]


class DeleteEvent(BaseEvent):
    pk: int
