from abc import ABC
from typing import Any, Dict

from src.property_finder.services.property_service import PropertyService
from src.property_finder.usecases import IUseCase


class BasePropertyUseCase(IUseCase, ABC):
    def __init__(self):
        self._service = PropertyService()


class CreatePropertyUseCase(BasePropertyUseCase):
    def execute(self, main_type: int, sub_type: int, title: str, description: str, agent: int):
        return self._service.create_property(main_type=main_type,
                                             sub_type=sub_type,
                                             title=title,
                                             description=description,
                                             agent=agent)


class GetPropertyUseCase(BasePropertyUseCase):
    def execute(self, pk: int):
        return self._service.find_property(pk=pk)


class UpdatePropertyUseCase(BasePropertyUseCase):
    def execute(self, pk: int, updates: Dict[str, Any]):
        return self._service.update_property(pk=pk, updates=updates)


class DeletePropertyUseCase(BasePropertyUseCase):
    def execute(self, pk: int):
        self._service.delete_property(pk=pk)


class SearchPropertyUseCase(BasePropertyUseCase):
    def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        return self._service.search_property(query=query, **kwargs)
