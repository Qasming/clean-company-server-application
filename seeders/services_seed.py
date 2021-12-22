from typing import List

from .seeder import Seeder

from data.repositories.services_repository import ServicesRepository

from business.services.models.service import Service
from business.services.models.additional_service import AdditionalService


class ServicesSeeder(Seeder):
    def seed(self):

        repository = ServicesRepository(self.db)

        share_additions_services: List[AdditionalService] = []

        clean_windows_additions_services: List[AdditionalService] = []

        additional_service = AdditionalService()
        additional_service.name = "Куханные шкафы"
        additional_service.price = 65000

        additional_service = repository.save_additional_service(additional_service)

        share_additions_services.append(additional_service)

        additional_service = AdditionalService()
        additional_service.name = "Внутри холодильника"
        additional_service.price = 70000

        additional_service = repository.save_additional_service(additional_service)

        share_additions_services.append(additional_service)

        additional_service = AdditionalService()
        additional_service.name = "Стирка белья"
        additional_service.price = 20000

        additional_service = repository.save_additional_service(additional_service)

        share_additions_services.append(additional_service)

        additional_service = AdditionalService()
        additional_service.name = "Внутри духовки"
        additional_service.price = 70000

        additional_service = repository.save_additional_service(additional_service)

        share_additions_services.append(additional_service)

        additional_service = AdditionalService()
        additional_service.name = "Глажка белья"
        additional_service.price = 50000

        additional_service = repository.save_additional_service(additional_service)

        share_additions_services.append(additional_service)

        additional_service = AdditionalService()
        additional_service.name = "Балкон"
        additional_service.price = 25000

        additional_service = repository.save_additional_service(additional_service)

        clean_windows_additions_services.append(additional_service)

        additional_service = AdditionalService()
        additional_service.name = "Оконные решетки"
        additional_service.price = 23000

        additional_service = repository.save_additional_service(additional_service)

        clean_windows_additions_services.append(additional_service)

        additional_service = AdditionalService()
        additional_service.name = "Мытье жалюзт"
        additional_service.price = 25000

        additional_service = repository.save_additional_service(additional_service)

        clean_windows_additions_services.append(additional_service)

        additional_service = AdditionalService()
        additional_service.name = "Сайдинг"
        additional_service.price = 48000

        additional_service = repository.save_additional_service(additional_service)

        clean_windows_additions_services.append(additional_service)

        service = Service()
        service.name = "Стандартная уборка"
        service.description = "Стандартная уборка все квартиры"
        service.price = 169000
        service.details = [
            '1-2 исполнителя',
            'удаляются легкие загрязнения',
            'высота до 1.8м',
            'работа от 2-4 часов'
        ]
        service.additional_services = [*share_additions_services]

        repository.save_service(service)

        service = Service()
        service.name = "Комплексная уборка"
        service.description = "Как поддерживающая, но на всю высоту"
        service.price = 269000
        service.details = [
            '1-2 исполнителя',
            'удаляются легкие загрязнения',
            'на всю высоту',
            'работа от 2-4 часов'
        ]
        service.additional_services = [*share_additions_services]

        repository.save_service(service)

        service = Service()
        service.name = "Мытье окон"
        service.description = "Чтобы окна сияли чистотой"
        service.price = 159000
        service.details = [
            '1-2 исполнителя',
            'моем окна в квартире, рамы, отливы, подокойники, москитные сетки',
            'работа от 2-5 часов'
        ]
        service.additional_services = [*clean_windows_additions_services]

        repository.save_service(service)

        service = Service()
        service.name = "Генеральная уборка"
        service.description = "Удалим все сложные загрязнения"
        service.price = 499000
        service.details = [
            '2-4 исполнителя',
            'удаляются любые загрязнения',
            'на всю высоту'
            'работа от 6-8 часов'
        ]

        service.additional_services = [*share_additions_services]

        repository.save_service(service)

        service = Service()
        service.name = "Уборка после ремонта"
        service.description = "Как генеральная и удалим следы ремонта"
        service.price = 699000
        service.details = [
            '2-4 исполнителя',
            'любые загрязнения и следы стройки',
            'на всю высоту'
            'работа от 6-8 часов'
        ]

        service.additional_services = [*share_additions_services]

        repository.save_service(service)


