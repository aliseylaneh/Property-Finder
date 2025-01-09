from abc import abstractmethod
from typing import Any, Dict, List, Tuple

from django_microservice_common.types.types import DjangoModelType

from src.property_finder.repositories import AbstractRepository


class ICRUDRepository(AbstractRepository):
    @abstractmethod
    async def all(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def filter_by_fields(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def create(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    @classmethod
    async def instance_update(cls,
                              instance: DjangoModelType,
                              fields: List[str],
                              data: Dict[str, Any]) -> Tuple[DjangoModelType, bool]:
        """
        Generic update service meant to be reused in local update repositories
        For example:
        def user_update(*, user: User, data) -> User:
            fields = ['first_name', 'last_name']
            user, has_updated = model_update(instance=user, fields=fields, data=data)
            // Do other actions with the user here
            return user
        Return value: Tuple with the following elements:
            1. The instance we updated
            2. A boolean value representing whether we performed an update or not.
        """
        has_updated = False
        for field in fields:
            # Skip if a field is not present in the actual data
            if field not in data:
                continue
            if getattr(instance, field) != data[field]:
                has_updated = True
                setattr(instance, field, data[field])
        # Perform an update only if any of the fields was actually changed
        if has_updated:
            instance.full_clean()
            # Update only the fields that are meant to be updated.
            # Django's docs reference:
            # https://docs.djangoproject.com/en/dev/ref/models/instances/#specifying-which-fields-to-save
            await instance.asave(update_fields=fields)
        return instance, has_updated
