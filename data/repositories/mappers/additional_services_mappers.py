from typing import List

from business.services.models.additional_service import AdditionalService


class AdditionalServicesMapper:
    @staticmethod
    def from_db_row_to_model(row) -> AdditionalService:
        service = AdditionalService()
        service.id = row['ID']
        service.price = int(row['price'])
        service.name = row['name']
        return service

    @staticmethod
    def from_db_rows_to_models(rows) -> List[AdditionalService]:
        services: List[AdditionalService] = []
        for row in rows:
            service = AdditionalServicesMapper.from_db_row_to_model(row)
            services.append(service)
        return services
