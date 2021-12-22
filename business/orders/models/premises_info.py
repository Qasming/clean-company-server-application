from enum import Enum


class PremisesInfo:
    class PremisesType(Enum):
        FLAT = 1,
        OFFICE = 2,
        HOUSE = 3

    area: int = 0
    address: str = ""
    premises_type: PremisesType = PremisesType.FLAT
