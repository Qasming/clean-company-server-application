from typing import List

from .dto.create_order_dto import CreateOrderDto
from .models.order import Order
from .models.premises_info import PremisesInfo
from .models.service_info import ServiceInfo
from .models.client_info import ClientInfo
from .models.additional_service_info import AdditionalServiceInfo
from .order_repository import OrderRepository


from ..services.services_service import ServicesService
from ..users.user_service import UserService


class OrderService:
    def __init__(self,
                 order_repository: OrderRepository,
                 services_service: ServicesService,
                 user_service: UserService
                 ):
        self._order_repository = order_repository
        self._services_service = services_service
        self._user_service = user_service

    def create_order(self, user_id: int, data: CreateOrderDto) -> Order:
        user = self._user_service.find_user_by_id(user_id)

        service = self._services_service.get_service_by_id(data.service_id)

        additional_services_info: List[AdditionalServiceInfo] = []

        for service_id in data.additional_services:
            for addition_service in service.additional_services:
                if addition_service.id == service_id:
                    additional_service_info = AdditionalServiceInfo()
                    additional_service_info.price = addition_service.price
                    additional_service_info.service = addition_service
                    additional_services_info.append(additional_service_info)
        order = Order()

        order.premises_info = PremisesInfo()
        order.premises_info.premises_type = data.premises_type
        order.premises_info.area = data.area
        order.premises_info.address = data.address

        order.client_info = ClientInfo()
        order.client_info.first_name = data.first_name
        order.client_info.last_name = data.last_name
        order.client_info.middle_name = data.middle_name
        order.client_info.phone = data.phone

        order.service_info = ServiceInfo()
        order.service_info.service = service
        order.service_info.service_price = service.price

        order.user = user
        order.additional_services = additional_services_info
        order.status = Order.Status.PENDING

        return self._order_repository.save(order)

    def get_order(self, order_id: int) -> Order:
        return self._order_repository.get_order(order_id)

    def cancel_order(self, order_id: int) -> Order:
        order = self._order_repository.get_order(order_id)
        order.cancel()
        order = self._order_repository.save(order)
        return order

    def complete_order(self, order_id: int) -> Order:
        order = self._order_repository.get_order(order_id)
        order.complete()
        order = self._order_repository.save(order)
        return order

    def get_user_orders(self, user_id: int) -> List[Order]:
        return self._order_repository.get_user_orders(user_id)
