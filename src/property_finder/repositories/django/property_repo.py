from typing import Any, Dict

from django.db import transaction
from django.db.models import QuerySet

from src.property_finder.models import Property
from src.property_finder.models.exceptions.property import PropertyNotFound
from src.property_finder.repositories.django.abstract_repository import ICRUDDjangoRepository


class PropertyDjangoRepository(ICRUDDjangoRepository):

    async def all(self) -> QuerySet[Property]:
        queryset = await Property.objects.prefetch_related("agent").all()
        return queryset

    async def filter_by_fields(self, data: Dict[str:Any]) -> QuerySet[Property]:
        queryset = await self.all()
        if not data:
            return queryset
        return queryset  # TODO implement filters

    async def find_by_id(self, pk: int) -> Property:
        instance = await Property.objects.filter(pk=pk).afirst()
        if not instance:
            raise PropertyNotFound()
        return instance

    async def create(self, main_type: int, sub_type: int, title: str, description: str, agent: int) -> Property:
        with transaction.atomic():
            instance = await Property.objects.acreate(main_type=main_type,
                                                      sub_type=sub_type,
                                                      title=title,
                                                      description=description,
                                                      agent=agent)
            return instance

    async def delete(self, pk: int):
        with transaction.atomic():
            await Property.objects.filter(pk=pk).adelete()

    async def update(self, pk: int, data: Dict[str, Any]) -> Property:
        with transaction.atomic():
            instance = await self.find_by_id(pk=pk)
            instance, is_updated = await self.instance_update(instance=instance,
                                                              data=data,
                                                              fields=list(data.keys()))
            return instance
