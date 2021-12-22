from typing import List


class CreateOrderDto:
    user_id: int
    service_id: int
    additional_services: List[int] = []
    address: str = ""
    area: int = 0
    premises_type: int = 1
    first_name: str = ""
    last_name: str = ""
    middle_name: str = ""
    phone: str = ""
