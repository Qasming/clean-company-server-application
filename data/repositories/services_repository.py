from typing import List

from business.services.models.additional_service import AdditionalService
from business.services.models.service import Service
from business.services.services_repository import ServicesRepository as ServicesRepositoryInterface
from business.services.exceptions import ServiceNotFoundException, AdditionalServiceNotFound

from .sqlite_repository import SqliteRepository
from .mappers.services_mappers import ServicesMapper
from .mappers.additional_services_mappers import AdditionalServicesMapper


class ServicesRepository(SqliteRepository, ServicesRepositoryInterface):
    def save_service(self, service: Service) -> Service:
        additional_services = service.additional_services
        service_details = service.details

        if service.id == 0:
            service = self.__create_service(service)
        else:
            service = self.__update_service(service)

        if service_details is not None:
            service.details = self.__save_service_details(service.id, service_details)

        if additional_services is not None:
            service.additional_services = self.__save_service_addition_services(service.id, additional_services)

        return service

    def get_all_services(self) -> List[Service]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM services")
        result = cursor.fetchall()
        cursor.close()
        services = ServicesMapper.from_db_rows_to_models(result)
        for service in services:
            service.details = self.__get_service_details(service.id)
        return services

    def get_service_by_id(self, service_id) -> Service:
        cursor = self.db.cursor()
        cursor.execute("""
                    SELECT * FROM services WHERE ID = :service_id
                """, {
            'service_id': service_id
        })

        data = cursor.fetchall()

        if len(data) == 0:
            raise ServiceNotFoundException()
        service = ServicesMapper.from_db_row_to_model(data[0])
        cursor.close()
        service.details = self.__get_service_details(service.id)
        service.additional_services = self.__get_additional_services_by_service_id(service.id)
        return service

    def save_additional_service(self, additional_service: AdditionalService):
        if additional_service.id == 0:
            return self.__create_additional_service(additional_service)
        else:
            return self.__update_additional_service(additional_service)

    def get_additional_service_by_id(self, additional_service_id: int) -> AdditionalService:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM additional_services WHERE ID = :service_id", {
            "service_id": additional_service_id
        })
        rows = cursor.fetchall()
        if len(rows) == 0:
            raise AdditionalServiceNotFound()
        return AdditionalServicesMapper.from_db_row_to_model(rows[0])

    def get_all_additional_services(self) -> List[AdditionalService]:
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT * FROM additional_services
        """)
        data = cursor.fetchall()
        cursor.close()
        return AdditionalServicesMapper.from_db_rows_to_models(data)

    def __create_service(self, service: Service) -> Service:
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO services 
            (name, price, description) VALUES 
            (:name, :price, :description)
        """, {
            'name': service.name,
            'price': service.price,
            'description': service.description
        })
        self.db.commit()
        cursor.execute("""
            SELECT * FROM services ORDER BY ID DESC LIMIT 1
        """)
        rows = cursor.fetchall()
        row = rows[0]
        cursor.close()
        return ServicesMapper.from_db_row_to_model(row)

    def __update_service(self, service: Service) -> Service:
        cursor = self.db.cursor()
        cursor.execute("""
                    UPDATE services
                    SET 
                    name = :name, 
                    price = :price, 
                    description = :description
                    WHERE ID = :id
                """, {
            'id': service.id,
            'name': service.name,
            'price': service.price,
            'description': service.description
        })

        self.db.commit()

        cursor.close()

        return self.get_service_by_id(service.id)

    def __get_service_details(self, service_id: int) -> List[str]:
        cursor = self.db.cursor()
        cursor.execute(
            """
                SELECT * FROM service_details WHERE service_id = :service_id
            """,
            {'service_id': service_id}
        )
        rows = cursor.fetchall()
        details: List[str] = []
        for row in rows:
            details.append(row['title'])
        cursor.close()
        return details

    def __save_service_details(self, service_id: int, details: List[str]) -> List[str]:
        cursor = self.db.cursor()

        cursor.execute("""
            DELETE FROM service_details WHERE service_id = :service_id
        """, {
            "service_id": service_id
        })
        self.db.commit()

        for detail in details:
            cursor.execute("""
                INSERT INTO service_details (
                    service_id, title
                ) VALUES (
                    :service_id,
                    :title
                )
            """, {
                "service_id": service_id,
                "title": detail
            })
            self.db.commit()
        cursor.close()

        return self.__get_service_details(service_id)

    def __save_service_addition_services(self,
                                         service_id: int,
                                         additions_services: List[AdditionalService]) -> List[AdditionalService]:
        cursor = self.db.cursor()
        cursor.execute("""
            DELETE FROM service_additional_services WHERE service_id = :service_id
        """, {
            "service_id": service_id
        })
        self.db.commit()

        for additions_service in additions_services:
            cursor.execute("""
                INSERT INTO service_additional_services (
                    service_id, additional_service_id
                ) VALUES (
                    :service_id,
                    :additional_service_id
                );
            """,{
                "service_id": service_id,
                "additional_service_id": additions_service.id
            })
            self.db.commit()
        cursor.close()

        return self.__get_additional_services_by_service_id(service_id)

    def __get_additional_services_by_service_id(self, service_id: int) -> List[AdditionalService]:
        cursor = self.db.cursor()
        cursor.execute("""
                    SELECT additional_services.ID, additional_services.name, additional_services.price FROM 
                    (	
                        service_additional_services
                        LEFT JOIN  additional_services
                        ON service_additional_services.additional_service_id = additional_services.ID
                    )
                    WHERE service_id = :service_id
                """, {
            'service_id': service_id
        })
        data = cursor.fetchall()
        cursor.close()
        return AdditionalServicesMapper.from_db_rows_to_models(data)

    def __create_additional_service(self, additional_service: AdditionalService) -> AdditionalService:
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO additional_services (
                name, price
            ) VALUES (
                :name,
                :price
            )
        """, {
            "name": additional_service.name,
            "price": additional_service.price
        })
        self.db.commit()
        cursor.execute("""
                    SELECT * FROM additional_services ORDER BY ID DESC LIMIT 1
                """)
        rows = cursor.fetchall()
        row = rows[0]
        cursor.close()
        return AdditionalServicesMapper.from_db_row_to_model(row)

    def __update_additional_service(self, additional_service: AdditionalService) -> AdditionalService:
        cursor = self.db.cursor()
        cursor.execute("""
                    UPDATE additional_service 
                    SET
                    name = :name,
                    price = :price,
                    WHERE ID = :additional_service_id
                """, {
            "name": additional_service.name,
            "price": additional_service.price,
            "additional_service_id": additional_service.id
        })
        self.db.commit()
        return self.get_additional_service_by_id(additional_service.id)
