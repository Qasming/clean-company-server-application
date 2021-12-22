import random
from typing import List

from .models.code import Code
from .repositories.code_repository import CodeRepository


class CodeService:
    def __init__(self, code_repository: CodeRepository):
        self._code_repository = code_repository

    def register_new_code(self, phone: str, user_id: int) -> Code:
        return self._code_repository.generate_code(phone, user_id)

    def disable_code(self, code: Code):
        self._code_repository.remove(code)

    def find_one(self, phone: str, code_value: str) -> Code:
        return self._code_repository.find_code(phone, code_value)
