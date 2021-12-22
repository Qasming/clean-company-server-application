from typing import List

from .services_repository import ServicesRepository
from .models.service import Service
from .models.additional_service import AdditionalService
from .dto.create_service_dto import CreateServiceDto
from .dto.update_service_dto import UpdateServiceDto


class ServicesService:
    def __init__(self, repository: ServicesRepository):
        self.repository = repository

    def create_service(self, data: CreateServiceDto) -> Service:
        service = Service()

        service.name = data.name

        service.price = data.price

        service.description = data.price

        service.additional_services = []

        service.details = data.details

        for additional_service_id in data.additional_services:

            additional_service = self.repository.get_additional_service_by_id(additional_service_id)

            service.additional_services.append(additional_service)

        return self.repository.save_service(service)

    def update_service(self, service_id: int, data: UpdateServiceDto) -> Service:
        service = self.repository.get_service_by_id(service_id)

        service.name = data.name

        service.price = data.price

        service.description = data.price

        service.additional_services = []

        service.details = data.details

        for additional_service_id in data.additional_services:

            additional_service = self.repository.get_additional_service_by_id(additional_service_id)

            service.additional_services.append(additional_service)

        return self.repository.save_service(service)

    def get_service_by_id(self, id: int) -> Service:
        return self.repository.get_service_by_id(id)

    def get_all_services(self) -> List[Service]:
        return self.repository.get_all_services()

    def get_service_additional_services(self, service_id: int) -> List[AdditionalService]:
        service = self.repository.get_service_by_id(service_id)
        return service.additional_services

    def get_all_additional_services(self) -> List[AdditionalService]:
        return self.repository.get_all_additional_services()
