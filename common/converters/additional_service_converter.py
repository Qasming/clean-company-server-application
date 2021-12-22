import json

from business.services.models.additional_service import AdditionalService
from typing import List


class AdditionalServiceConverter:
    @staticmethod
    def service_to_json(service: AdditionalService):
        return {
            'id': service.id,
            'name': service.name,
            'price': service.price
        }

    @staticmethod
    def service_list_to_json(services: List[AdditionalService]) -> [AdditionalService]:
        json_list = []
        for service in services:
            json_list.append(AdditionalServiceConverter.service_to_json(service))
        return json.dumps(json_list)
