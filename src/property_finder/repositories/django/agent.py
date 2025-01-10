from typing import Any, Dict

from django.db import transaction
from django.db.models import QuerySet

from property_finder.repositories.django.services import instance_update as InstanceUpdateService
from src.property_finder.models import Agent
from src.property_finder.models.exceptions.agent import AgentNotFound


class AgentDjangoRepository:

    def all(self) -> QuerySet[Agent]:
        queryset = Agent.objects.prefetch_related("agent").all()
        return queryset

    def find_by_id(self, pk: int) -> Agent:
        instance = Agent.objects.filter(pk=pk).first()
        if not instance:
            raise AgentNotFound()
        return instance

    def create(self, name: str, email: str, phone_number: str) -> Agent:
        with transaction.atomic():
            instance = Agent.objects.create(name=name, email=email, phone_number=phone_number)
            return instance

    def delete(self, pk: int):
        with transaction.atomic():
            Agent.objects.filter(pk=pk).delete()

    def update(self, pk: int, updates: Dict[str, Any]) -> Agent:
        with transaction.atomic():
            instance = self.find_by_id(pk=pk)
            instance, is_updated = InstanceUpdateService(instance=instance,
                                                         data=updates,
                                                         fields=list(updates.keys()))
            return instance
