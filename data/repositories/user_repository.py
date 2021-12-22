from typing import List

from business.users.dto.create_user_dto import CreateUserDto
from business.users.dto.update_user_dto import UpdateUserDto
from business.users.models.user import User
from business.users.user_respository import UserRepository as UserRepositoryInterface
from business.users.exceptions import UserNotFound

from .mappers.users_mapper import UsersMapper

from .sqlite_repository import SqliteRepository


class UserRepository(SqliteRepository, UserRepositoryInterface):
    def save(self, user: User) -> User:
        if user.id == 0:
            data = CreateUserDto()
            data.phone = user.phone
            return self.create_user(data)
        else:
            data = UpdateUserDto()
            data.phone = user.phone
            data.email = user.email
            data.first_name = user.first_name
            data.last_name = user.last_name
            data.middle_name = user.middle_name
            return self.update_user(user.id, data)

    def update_user(self, user_id: int, update_user_dto: UpdateUserDto) -> User:
        cursor = self.db.cursor()
        cursor.execute("""
            UPDATE users 
            SET 
            first_name = :first_name,
            last_name = :last_name,
            middle_name = :middle_name,
            email = :email
            WHERE ID = :user_id;
        """, {
            'first_name': update_user_dto.first_name,
            'last_name': update_user_dto.last_name,
            'middle_name': update_user_dto.middle_name,
            'email': update_user_dto.email,
            'user_id': user_id
        })
        self.db.commit()
        cursor.close()
        return self.find_user_by_id(user_id)

    def find_user_by_id(self, id: int) -> User:
        users = self.find_all()
        for user in users:
            if user.id == id:
                return user
        raise UserNotFound()

    def find_user_by_phone(self, phone: str) -> User:
        users = self.find_all()
        for user in users:
            if user.phone == phone:
                return user
        raise UserNotFound()

    def create_user(self, data: CreateUserDto) -> User:
        cursor = self.db.cursor()

        cursor.execute("""
            INSERT INTO users (phone) VALUES (:phone)
        """, {
            'phone': data.phone
        })
        self.db.commit()

        cursor.execute("SELECT * FROM users ORDER BY ID DESC LIMIT 1")

        rows = cursor.fetchall()

        cursor.close()

        user = UsersMapper.from_db_row_to_model(rows[0])
        return user

    def find_all(self) -> List[User]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        cursor.close()
        users = UsersMapper.from_db_rows_to_models(rows)
        return users

