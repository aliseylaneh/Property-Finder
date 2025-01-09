from typing import Any, Dict

from django.db import transaction
from django.db.models import QuerySet

from src.property_finder.models import Agent
from src.property_finder.models.exceptions.agent import AgentNotFound
from src.property_finder.repositories.django.base_repo import ICRUDRepository


class AgentRepository(ICRUDRepository):
    async def all(self) -> QuerySet[Agent]:
        queryset = await Agent.objects.prefetch_related("agent").all()
        return queryset

    async def filter_by_fields(self, data: Dict[str:Any]) -> QuerySet[Agent]:
        queryset = await self.all()
        if not data:
            return queryset
        return queryset  # TODO implement filters

    async def find_by_id(self, pk: int) -> Agent:
        instance = await Agent.objects.filter(pk=pk).afirst()
        if not instance:
            raise AgentNotFound()
        return instance

    async def create(self, name: str, email: str, phone_number: str) -> Agent:
        with transaction.atomic():
            instance = await Agent.objects.acreate(name=name, email=email, phone_number=phone_number)
            return instance

    async def delete(self, pk: int):
        with transaction.atomic():
            await Agent.objects.filter(pk=pk).adelete()

    async def update(self, pk: int, data: Dict[str, Any]) -> Agent:
        with transaction.atomic():
            instance = await self.find_by_id(pk=pk)
            instance, is_updated = await self.instance_update(instance=instance,
                                                              data=data,
                                                              fields=list(data.keys()))
            return instance
