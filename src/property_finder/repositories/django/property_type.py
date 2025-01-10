from django.db.models import QuerySet

from src.property_finder.models import Property, PropertyType
from src.property_finder.repositories.django.base import BaseRepository


class PropertyTypeRepository(BaseRepository):

    def all(self) -> QuerySet[Property]:
        return PropertyType.objects.all()
