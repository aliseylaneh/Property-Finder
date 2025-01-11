from typing import Tuple

from django.db.models import QuerySet

from src.property_finder.models.exceptions.property_type import MainTypeNotFound, PropertyTypeErrorAssignment, PropertyTypeNotFound, \
    SubTypeNotFound
from src.property_finder.models import PropertyType


class PropertyTypeRepository:

    def get_all(self) -> QuerySet[PropertyType]:
        return PropertyType.objects.all()

    def find_by_id(self, pk: int) -> PropertyType:
        instance = PropertyType.objects.filter(id=pk).filter()
        if not instance:
            raise PropertyTypeNotFound()
        return instance

    def get_required_types(self, main_type: int | None, sub_type: int | None) -> Tuple[PropertyType, PropertyType]:
        """
        This function will two Property types as maintype and subtype and checkout out if they exist.
        :raise PropertyTypeErrorAssignment: If you try to assign the same type for maintype and subtype
        :raise MainTypeNotFound: If you try to assign a type that doesn't exist
        :raise SubTypeNotFound: If you try to assign a type that doesn't exist
        :return: Tuple[PropertyType, PropertyType] which include validated main and subtype
        """
        if main_type == sub_type:
            raise PropertyTypeErrorAssignment()
        query = PropertyType.objects.filter(id__in=[main_type, sub_type]).order_by('depth')
        existing_ids = query.values_list('id', flat=True)
        if main_type:
            if main_type not in existing_ids:
                raise MainTypeNotFound()
        if sub_type:
            if sub_type not in existing_ids:
                raise SubTypeNotFound()
        return query[0], query[1]
