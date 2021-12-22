from typing import List

from business.orders.models.order import Order
from business.orders.models.premises_info import PremisesInfo


class OrderConverter:
    @staticmethod
    def from_model_to_json(order: Order) -> dict:
        order_json = {}

        order_json['id'] = order.id

        if order.status == Order.Status.PENDING:
            order_json['status'] = 1

        elif order.status == Order.Status.COMPLETED:
            order_json['status'] = 2

        elif order.status == Order.Status.CANCELED:
            order_json['status'] = 3

        order_json['premises_info'] = {
            'area': order.premises_info.area,
            'address': order.premises_info.address,
            'premises_type': order.premises_info.premises_type.value
        }

        if order.premises_info.premises_type == PremisesInfo.PremisesType.FLAT:
            order_json['premises_info']['premises_type'] = 1
        elif order.premises_info.premises_type == PremisesInfo.PremisesType.OFFICE:
            order_json['premises_info']['premises_type'] = 2
        elif order.premises_info.premises_type == PremisesInfo.PremisesType.HOUSE:
            order_json['premises_info']['premises_type'] = 3

        order_json['client_info'] = {
            'first_name': order.client_info.first_name,
            'last_name': order.client_info.last_name,
            'middle_name': order.client_info.middle_name,
            'phone': order.client_info.phone
        }

        order_json['service_info'] = {
            'id': order.service_info.service.id,
            'name': order.service_info.service.name,
            'price': order.service_info.service_price
        }

        order_json['additional_services'] = []

        for additional_service in order.additional_services:
            additional_service_dto = {
                'id': additional_service.service.id,
                'name': additional_service.service.name,
                'price': additional_service.price
            }
            order_json['additional_services'].append(additional_service_dto)

        order_json['sum'] = order.sum

        return order_json

    @staticmethod
    def from_list_model_to_json(orders:List[Order]):
        orders_dto = []
        for order in orders:
            dto = OrderConverter.from_model_to_json(order)
            orders_dto.append(dto)
        return orders_dto
