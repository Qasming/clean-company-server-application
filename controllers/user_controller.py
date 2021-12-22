from flask_jwt_extended import get_jwt_identity
from flask import Request, Response

from common.converters.user_converter import UserConverter

from business.users.user_service import UserService
from business.users.dto.update_user_dto import UpdateUserDto

from common.converters.user_converter import UserConverter


class UserController:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    def get_all(self):
        return UserConverter.user_list_to_json(self._user_service.find_all())

    def get_one(self, id: int):
        user = self._user_service.find_user_by_id(id)
        if user is None:
            return {'msg': 'User not found'}, 404
        return UserConverter.user_to_json(user)

    def update_user(self, request: Request):
        user_id = get_jwt_identity()
        data = UpdateUserDto()
        data.last_name = request.json['last_name']
        data.first_name = request.json['first_name']
        data.middle_name = request.json['middle_name']
        data.email = request.json['email']
        user = self._user_service.update_user(user_id, data)
        return UserConverter.user_to_json(user)
