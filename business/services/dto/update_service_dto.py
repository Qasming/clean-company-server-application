from typing import List


class UpdateServiceDto:
    name: str = ""
    description: str = ""
    price: int = 0
    details: List[str] = None
    additional_services: List[int] = None
