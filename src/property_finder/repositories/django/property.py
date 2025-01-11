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
        """
        PropertyDjangoRepository is the implementation of layer which talks with model layer
        and has the responsibility to do all operations on database using Django ORM.
        It has two dependency:
        1. AgentDjangoRepository for database operations on Agent models
        2. PropertyRepository for database operations on Property Type models
        """
        self._agent_repository = AgentDjangoRepository()
        self._property_type_repository = PropertyTypeRepository()

    def all(self) -> QuerySet[Property]:
        """
        This function returns all Properties in the database.
        :return: QuerySet of all Properties in the database.
        """
        queryset = Property.objects.select_related("agent", "main_type", "sub_type").all()
        return queryset

    def find_by_id(self, pk: int) -> Property:
        """
        This function retrieve a Property instance by the given Property ID.
        :param pk: Property ID
        :return: Property instance
        """
        instance = Property.objects.select_related("agent", "main_type", "sub_type").filter(pk=pk).first()
        if not instance:
            raise PropertyNotFound()
        return instance

    def create(self, main_type: int, sub_type: int, title: str, description: str, agent: int) -> Property:
        """
        This function create Property instance,
        1. Validate existence of given main_type and sub_type
        2. Validate existence of given agent_id
        3. Create the Property instance and save it to database
        :param main_type: The ID of the Property type with a MAIN_TYPE property
        :param sub_type: The ID of the Property type with a SUB_TYPE property
        :param title: The title of the Property
        :param description: The description of the Property
        :param agent: The ID of the Agent which the Property instance belongs.
        :return: Property instance
        """
        with transaction.atomic():
            self._property_type_repository.check_main_sub_exists(main_type=main_type, sub_type=sub_type)
            self._agent_repository.check_agent_exists(pk=agent)
            instance = Property.objects.create(main_type_id=main_type, sub_type_id=sub_type, title=title, description=description,agent_id=agent)
            return instance

    def delete(self, pk: int):
        """
        Delete the Property with the given pk
        :param pk: Property ID
        """
        with transaction.atomic():
            Property.objects.filter(pk=pk).delete()

    def update(self, pk: int, updates: Dict[str, Any]) -> Property:
        """
        This function updates Property instance,
        1. Validate existence of given main_type and sub_type
        2. Validate existence of given agent_id
        3. Update the Property instance
        :param pk: Property ID
        :param updates: A dictionary that includes fields of Property instance with new values.
        :return: Property instance
        """
        with transaction.atomic():
            instance = self.find_by_id(pk=pk)
            self._property_type_repository.check_main_sub_exists(main_type=updates.get('main_type_id', None),sub_type=updates.get('sub_type_id', None))
            self._agent_repository.check_agent_exists(pk=updates.get('agent_id', None))
            instance, is_updated = InstanceUpdateService(instance=instance, data=updates, fields=list(updates.keys()))
            return instance
