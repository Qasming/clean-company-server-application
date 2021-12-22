import json
from typing import List

from business.users.models.user import User


class UserConverter:
    @staticmethod
    def user_to_json(user: User):
        return {
            "id": user.id,
            "phone": user.phone,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "middle_name": user.middle_name,
            "email": user.email
        }

    @staticmethod
    def user_list_to_json(users: List[User]):
        user_list = []
        for user in users:
            user_list.append(UserConverter.user_to_json(user))
        return json.dumps(user_list)
