from abc import ABC

from src.property_finder.services.property_service import PropertyService
from src.property_finder.usecases import IUseCase


class BasePropertyUseCase(IUseCase, ABC):
    def __init__(self):
        self._service = PropertyService()


class CreatePropertyUseCase(BasePropertyUseCase):
    def execute(self, main_type: int, sub_type: int, title: str, description: str, agent: int):
        self._service.create_property(main_type=main_type,
                                      sub_type=sub_type,
                                      title=title,
                                      description=description,
                                      agent=agent)
