from typing import List
from .additional_service import AdditionalService


class Service:
    id: int = 0
    name: str = ""
    description: str = ""
    price: int = 0
    additional_services: List[AdditionalService] = None
    details: List[str] = None
