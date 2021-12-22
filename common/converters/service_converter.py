import json

from business.services.models.service import Service
from typing import List


class ServiceConverter:
    @staticmethod
    def service_to_json(service: Service):
        return {
            'id': service.id,
            'name': service.name,
            'description': service.description,
            'price': service.price,
            'details': service.details
        }

    @staticmethod
    def service_list_to_json(services: List[Service]) -> [Service]:
        json_list = []
        for service in services:
            json_list.append(ServiceConverter.service_to_json(service))
        return json.dumps(json_list)
