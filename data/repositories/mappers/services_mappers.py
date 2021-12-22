from typing import List

from business.services.models.service import Service


class ServicesMapper:
    @staticmethod
    def from_db_row_to_model(row) -> Service:
        service = Service()
        service.id = row['ID']
        service.description = row['description']
        service.price = int(row['price'])
        service.name = row['name']
        return service

    @staticmethod
    def from_db_rows_to_models(rows) -> List[Service]:
        services: List[Service] = []
        for row in rows:
            service = ServicesMapper.from_db_row_to_model(row)
            services.append(service)
        return services
