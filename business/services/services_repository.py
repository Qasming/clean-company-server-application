from abc import abstractmethod
from typing import List

from .models.service import Service
from .models.additional_service import AdditionalService


class ServicesRepository:

    # Services

    @abstractmethod
    def save_service(self, service: Service):
        pass

    @abstractmethod
    def get_all_services(self) -> List[Service]:
        pass

    @abstractmethod
    def get_service_by_id(self, service_id: int) -> Service:
        pass

    # Additional Services

    @abstractmethod
    def save_additional_service(self, additional_service: AdditionalService):
        pass

    @abstractmethod
    def get_additional_service_by_id(self, additional_service_id: int) -> AdditionalService:
        pass

    @abstractmethod
    def get_all_additional_services(self) -> List[AdditionalService]:
        pass
