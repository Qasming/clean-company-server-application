from typing import List

from business.users.models.user import User


class UsersMapper:
    @staticmethod
    def from_db_row_to_model(row: dict) -> User:
        user = User()
        user.id = int(row['ID'])
        user.phone = str(row['phone'])

        if row['first_name'] is not None:
            user.first_name = str(row['first_name'])
        else:
            user.first_name = ""

        if row['last_name'] is not None:
            user.last_name = str(row['last_name'])
        else:
            user.last_name = ""

        if row['middle_name'] is not None:
            user.middle_name = str(row['middle_name'])
        else:
            user.middle_name = ""

        if row['email'] is not None:
            user.email = str(row['email'])
        else:
            user.email = ""

        return user

    @staticmethod
    def from_db_rows_to_models(rows: List[dict]) -> List[User]:
        users: List[User] = []
        for row in rows:
            user = UsersMapper.from_db_row_to_model(row)
            users.append(user)
        return users
