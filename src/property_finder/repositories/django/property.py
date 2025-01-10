from typing import Any, Dict

from django.db import transaction
from django.db.models import QuerySet

from property_finder.repositories.django.agent import AgentDjangoRepository
from property_finder.repositories.django.property_type import PropertyTypeRepository
from property_finder.repositories.django.services import instance_update as InstanceUpdateService
from src.property_finder.models import Property
from src.property_finder.models.exceptions.property import PropertyNotFound


class PropertyDjangoRepository:
    def __init__(self):
        self._agent_repository = AgentDjangoRepository()
        self._property_type_repository = PropertyTypeRepository()

    def all(self) -> QuerySet[Property]:
        queryset = Property.objects.prefetch_related("agent", "main_type", "sub_type").all()
        return queryset

    def find_by_id(self, pk: int) -> Property:
        instance = Property.objects.select_related("agent", "main_type", "sub_type").filter(pk=pk).first()
        if not instance:
            raise PropertyNotFound()
        return instance

    def create(self, main_type: int, sub_type: int, title: str, description: str, agent: int) -> Property:
        with transaction.atomic():
            self._property_type_repository.check_main_sub_exists(main_type=main_type, sub_type=sub_type)
            self._agent_repository.find_by_id(pk=agent)
            instance = Property.objects.create(main_type_id=main_type,
                                               sub_type_id=sub_type,
                                               title=title,
                                               description=description,
                                               agent_id=agent)
            return instance

    def delete(self, pk: int):
        with transaction.atomic():
            Property.objects.filter(pk=pk).delete()

    def update(self, pk: int, updates: Dict[str, Any]) -> Property:
        with transaction.atomic():
            self._property_type_repository.check_main_sub_exists(main_type=updates['agent'], sub_type=updates['sub_type'])
            self._agent_repository.find_by_id(pk=updates['agent'])
            instance = self.find_by_id(pk=pk)
            instance, is_updated = InstanceUpdateService(instance=instance,
                                                         data=updates,
                                                         fields=list(updates.keys()))
            return instance
