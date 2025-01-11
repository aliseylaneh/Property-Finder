from enum import StrEnum
from typing import Any, Dict

from pydantic import BaseModel

from property_finder.models.types.types import RepositoryModelType


class DomainEventTypes(StrEnum):
    PROPERTY_UPDATED = "PROPERTY_UPDATED"


class UpdateEvent(BaseModel):
    pk: int
    repo_name: RepositoryModelType
    updates: Dict[str, Any]
    event_type: DomainEventTypes
