from flask import Request, Response

from typing import List

from business.services.models.service import Service
from business.services.services_service import ServicesService
from business.services.dto.create_service_dto import CreateServiceDto
from business.services.dto.update_service_dto import UpdateServiceDto
from business.services.exceptions import ServiceNotFoundException

from common.converters.service_converter import ServiceConverter
from common.converters.additional_service_converter import AdditionalServiceConverter


class ServiceController:
    def __init__(self, services_service: ServicesService):
        self._services_service = services_service

    def get_all_services(self) -> List[Service]:
        services = self._services_service.get_all_services()
        return ServiceConverter.service_list_to_json(services)

    def get_service_by_id(self, service_id: int):
        try:
            service = self._services_service.get_service_by_id(service_id)
            return ServiceConverter.service_to_json(service)
        except ServiceNotFoundException:
            return {'msg': "Service not found"}, 404

    def get_service_additional_services(self, service_id: int):
        try:
            additional_services = self._services_service.get_service_additional_services(service_id)
            print(additional_services)
            return AdditionalServiceConverter.service_list_to_json(additional_services)
        except ServiceNotFoundException:
            return {'msg': "Service not found"}, 404

    def create(self, request: Request):
        data = CreateServiceDto()
        data.name = request.json['name']
        data.price = int(request.json['price'])
        data.description = request.json['description']
        service = self._services_service.create_service(data)
        return ServiceConverter.service_to_json(service), 201

    def update(self, id: int, request: Request):
        data = UpdateServiceDto()
        data.name = request.json['name']
        data.price = int(request.json['price'])
        data.description = request.json['description']
        service = self._services_service.update_service(id, data)
        return ServiceConverter.service_to_json(service), 201

