from .models.code import Code
from .exceptions.unauthorized_exception import UnauthorizedExceptions

from .code_service import CodeService

from ..users.user_service import UserService
from ..users.dto.create_user_dto import CreateUserDto
from ..users.models.user import User
from ..users.exceptions import UserNotFound


class AuthService:
    def __init__(self,
                 code_service: CodeService,
                 user_service: UserService
                 ):
        self._code_service: CodeService = code_service
        self._user_service = user_service

    def login(self, phone: str, code: str) -> User:
        c = self._code_service.find_one(phone, code)
        if c is None:
            raise UnauthorizedExceptions()
        self._code_service.disable_code(c)
        return self._user_service.find_user_by_id(c.user_id)

    def register_code(self, phone: str) -> Code:
        try:
            user = self._user_service.find_user_by_phone(phone)
        except UserNotFound:
            data = CreateUserDto()
            data.phone = phone
            user = self._user_service.create_user(data)
        code = self._code_service.register_new_code(phone, user.id)
        return code
