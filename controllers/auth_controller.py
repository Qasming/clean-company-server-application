import flask_jwt_extended

from business.users.user_service import UserService
from business.auth.auth_service import AuthService
from business.auth.exceptions.unauthorized_exception import UnauthorizedExceptions
from business.users.exceptions import UserNotFound

from flask import Request, jsonify
from config import DEBUG_MODE, SMS_RU_ID
from common.converters.user_converter import UserConverter

from http.client import HTTPSConnection, HTTPConnection


class AuthController:
    def __init__(self, auth_service: AuthService, user_service: UserService):
        self._auth_service = auth_service
        self._user_service = user_service

    def get_code(self, request: Request):
        phone = str(request.json['phone'])
        code = self._auth_service.register_code(phone)

        if DEBUG_MODE:
            return {
                'code': code.value
            }
        self.send_sms(phone, "Code: " + code.value)
        return {'mes': "Message sent"}

    def login(self, request: Request):
        phone = str(request.json['phone'])
        code = str(request.json['code'])
        try:
            user = self._auth_service.login(phone, code)
            access_token = flask_jwt_extended.create_access_token(user.id)
            return jsonify({'access_token': access_token})
        except UnauthorizedExceptions:
            return jsonify({'msg': 'Unauthorized error'}), 401

    def me(self):
        user_id = flask_jwt_extended.get_jwt_identity()
        try:
            user = self._user_service.find_user_by_id(user_id)
            return UserConverter.user_to_json(user)
        except UserNotFound:
            return jsonify({'msg': 'Unauthorized error'}), 401

    def send_sms(self, phone: str, message: str):
        connection = HTTPSConnection("sms.ru")
        mes = ""
        for lit in message:
            if lit == ' ':
                mes += '+'
            else:
                mes += lit

        connection.request("POST", "/sms/send?api_id="
                     + SMS_RU_ID +
                     "&to=" + phone +
                     "&msg=" + mes
        )
        connection.getresponse()
