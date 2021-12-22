from business.auth.models.code import Code
from business.auth.repositories.code_repository import CodeRepository as RepositoryInterface

from .code_store import CodeStore


class CodeRepository(RepositoryInterface):
    def __init__(self, code_store: CodeStore):
        self._code_store = code_store

    def generate_code(self, phone: str, user_id: int) -> Code:
        return self._code_store.register_code(phone, user_id)

    def find_code(self, phone: str, code: str) -> Code:
        return self._code_store.find_code(phone, code)

    def remove(self, code: Code) -> None:
        return self._code_store.remove_code(code)

