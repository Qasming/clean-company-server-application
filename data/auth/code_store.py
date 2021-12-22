import random
from typing import List

from business.auth.models.code import Code


class CodeStore:
    def __init__(self):
        self._codes: List[Code] = []

    def register_code(self, phone: str, user_id: int) -> Code:
        while True:
            code_value = str(random.randint(1000, 9999))
            code = self.find_code(phone, code_value)
            if code is None:
                new_code = Code()
                new_code.user_id = user_id
                new_code.phone = phone
                new_code.value = code_value
                self._codes.append(new_code)
                return new_code

    def remove_code(self, code: Code) -> None:
        for c in self._codes:
            if c.phone == code.phone and c.value == c.value and c.user_id == code.user_id:
                self._codes.remove(c)

    def find_code(self, phone: str, code: str) -> Code:
        for c in self._codes:
            if c.phone == phone and c.value == code:
                return c
        return None
