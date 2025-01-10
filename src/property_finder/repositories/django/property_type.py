from django.db.models import QuerySet

from property_finder.models.exceptions.property_type import MainTypeNotFound, PropertyTypeNotFound, SubTypeNotFound
from src.property_finder.models import PropertyType


class PropertyTypeRepository:

    def get_all(self) -> QuerySet[PropertyType]:
        return PropertyType.objects.all()

    def find_by_id(self, pk: int) -> PropertyType:
        instance = PropertyType.objects.filter(id=pk).filter()
        if not instance:
            raise PropertyTypeNotFound()
        return instance

    def check_main_sub_exists(self, main_type: id, sub_type: id):
        """
        This function will two Property types as maintype and subtype and checkout out if they exist.
        """
        existing_ids = PropertyType.objects.filter(id__in=[main_type, sub_type]).values_list('id', flat=True)
        print(existing_ids)
        if main_type not in existing_ids:
            raise MainTypeNotFound()
        if sub_type not in existing_ids:
            raise SubTypeNotFound()
