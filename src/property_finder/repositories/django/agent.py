from typing import Any, Dict

from django.db import transaction
from django.db.models import QuerySet

from property_finder.repositories.django.services import instance_update as InstanceUpdateService
from src.property_finder.models import Agent
from src.property_finder.models.exceptions.agent import AgentNotFound, InvalidPrimaryKey


class AgentDjangoRepository:

    def all(self) -> QuerySet[Agent]:
        """
        Returns all agents from the database.
        :return: QuerySet[Agent] of Agent instances.
        """
        queryset = Agent.objects.prefetch_related("agent").all()
        return queryset

    def check_agent_exists(self, pk: int | None):
        """
        Check if an agent exists without returning any value.
        :param pk: Agent ID to check or None.
        """
        if pk:
            instance = Agent.objects.filter(pk=pk).first()
            if not instance:
                raise AgentNotFound()

    def find_by_id(self, pk: int | None) -> Agent:
        """
        Retrieve an agent by its dedicated ID.
        :param pk: Agent ID which must be Integer.
        :return: The retrieved instance of Agent.
        """
        if not pk:
            raise InvalidPrimaryKey()
        instance = Agent.objects.filter(pk=pk).first()
        if not instance:
            raise AgentNotFound()
        return instance

    def create(self, name: str, email: str, phone_number: str) -> Agent:
        """
        Creates a new agent with below params:
        :param name: The name of the agent which is string.
        :param email: The email address of the agent which is string.
        :param phone_number: The phone number of the agent which is string.
        :return: The created instance of Agent.
        """
        with transaction.atomic():
            instance = Agent.objects.create(name=name, email=email, phone_number=phone_number)
            return instance

    def delete(self, pk: int):
        """
        Deletes an agent by its dedicated ID.
        :param pk: Agent ID to delete.
        """
        with transaction.atomic():
            Agent.objects.filter(pk=pk).delete()

    def update(self, pk: int, updates: Dict[str, Any]) -> Agent:
        """
        Update an agent by a given dictionary of fields and their values
        :param pk: Agent ID to update.
        :param updates: Dictionary of Agent fields and their new values.
        """
        with transaction.atomic():
            instance = self.find_by_id(pk=pk)
            instance, is_updated = InstanceUpdateService(instance=instance, data=updates, fields=list(updates.keys()))
            return instance
