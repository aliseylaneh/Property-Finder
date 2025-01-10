from typing import Any, Dict

from django.db import transaction
from django.db.models import QuerySet

from src.property_finder.models import Property
from src.property_finder.models.exceptions.property import PropertyNotFound
from src.property_finder.repositories.django.base import BaseRepository


class PropertyDjangoRepository(BaseRepository):

    def all(self) -> QuerySet[Property]:
        queryset = Property.objects.prefetch_related("agent").all()
        return queryset

    def find_by_id(self, pk: int) -> Property:
        instance = Property.objects.filter(pk=pk).first()
        if not instance:
            raise PropertyNotFound()
        return instance

    def create(self, main_type: int, sub_type: int, title: str, description: str, agent: int) -> Property:
        with transaction.atomic():
            instance = Property.objects.create(main_type_id=main_type,
                                               sub_type_id=sub_type,
                                               title=title,
                                               description=description,
                                               agent_id=agent)
            return instance

    def delete(self, pk: int):
        with transaction.atomic():
            Property.objects.filter(pk=pk).delete()

    def update(self, pk: int, data: Dict[str, Any]) -> Property:
        with transaction.atomic():
            instance = self.find_by_id(pk=pk)
            instance, is_updated = self.instance_update(instance=instance,
                                                        data=data,
                                                        fields=list(data.keys()))
            return instance
