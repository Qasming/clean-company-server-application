from abc import abstractmethod

from ..models.code import Code


class CodeRepository:
    @abstractmethod
    def find_code(self, phone: str, code: str) -> Code:
        pass

    @abstractmethod
    def remove(self, code: Code) -> None:
        pass

    @abstractmethod
    def generate_code(self, phone: str, user_id: int) -> Code:
        pass
