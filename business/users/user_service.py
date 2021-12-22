from typing import List

from .user_respository import UserRepository
from .models.user import User
from .dto.create_user_dto import CreateUserDto
from .dto.update_user_dto import UpdateUserDto


class UserService:
    def __init__(self, repository: UserRepository):
        self._user_repository = repository

    def find_user_by_id(self, id: int) -> User:
        return self._user_repository.find_user_by_id(id)

    def create_user(self, data: CreateUserDto) -> User:
        user = User()

        user.phone = data.phone

        return self._user_repository.save(user)

    def update_user(self, user_id: int, data: UpdateUserDto):
        user = self._user_repository.find_user_by_id(user_id)
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.middle_name = data.middle_name
        user.email = data.email
        return self._user_repository.save(user)

    def find_user_by_phone(self, phone: str) -> User:
        return self._user_repository.find_user_by_phone(phone)

    def find_all(self) -> List[User]:
        return self._user_repository.find_all()

