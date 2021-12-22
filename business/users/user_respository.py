from abc import abstractmethod
from typing import List

from .models.user import User
from .dto.create_user_dto import CreateUserDto
from .dto.update_user_dto import UpdateUserDto


class UserRepository:
    @abstractmethod
    def find_user_by_id(self, id: int) -> User:
        pass

    @abstractmethod
    def find_user_by_phone(self, phone: str) -> User:
        pass

    @abstractmethod
    def create_user(self, data: CreateUserDto) -> User:
        pass

    @abstractmethod
    def find_all(self) -> List[User]:
        pass

    @abstractmethod
    def update_user(self, user_id: int, update_user_dto: UpdateUserDto) -> User:
        pass

    @abstractmethod
    def save(self, user: User):
        pass
