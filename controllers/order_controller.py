import flask

from business.orders.order_service import OrderService
from business.orders.dto.create_order_dto import CreateOrderDto

from flask import Request, Response, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from config import DEBUG_MODE

from common.converters.order_converter import OrderConverter


class OrderController:
    def __init__(self, order_service: OrderService):
        self._order_service = order_service

    def create_order(self, request: Request):
        user_id = get_jwt_identity()
        data = CreateOrderDto()
        data.area = int(request.json['area'])
        data.service_id = int(request.json['service_id'])
        data.additional_services = request.json['additional_services']
        data.address = request.json['address']
        data.first_name = request.json['client_first_name']
        data.last_name = request.json['client_last_name']
        data.middle_name = request.json['client_middle_name']
        data.phone = request.json['phone']
        data.user_id = user_id
        data.premises_type = int(request.json['premises_type'])
        order = self._order_service.create_order(user_id, data)
        return flask.jsonify({'id': order.id}), 201

    def get_user_orders(self):
        user_id = get_jwt_identity()
        orders = self._order_service.get_user_orders(user_id)
        return flask.jsonify(OrderConverter.from_list_model_to_json(orders))

    def get_order(self, order_id: int):
        order = self._order_service.get_order(order_id)
        return flask.jsonify(OrderConverter.from_model_to_json(order))

    def cancel_order(self, order_id: int):
        order = self._order_service.cancel_order(order_id)
        return flask.jsonify(OrderConverter.from_model_to_json(order))

    def complete_order(self, order_id: int):
        order = self._order_service.complete_order(order_id)
        return flask.jsonify(OrderConverter.from_model_to_json(order))

