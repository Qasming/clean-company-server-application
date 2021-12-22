from typing import List
from enum import Enum

from ...users.models.user import User
from .client_info import ClientInfo
from .service_info import ServiceInfo
from .premises_info import PremisesInfo
from .additional_service_info import AdditionalServiceInfo


class Order:
    class Status(Enum):
        PENDING = 1
        COMPLETED = 2
        CANCELED = 3
    id: int = 0
    user: User
    additional_services: List[AdditionalServiceInfo] = []
    status: Status = Status.PENDING
    service_info: ServiceInfo
    client_info: ClientInfo
    premises_info: PremisesInfo

    def cancel(self):
        self.status = Order.Status.CANCELED

    def complete(self):
        self.status = Order.Status.COMPLETED

    @property
    def sum(self) -> int:
        s = self.service_info.service_price
        for asi in self.additional_services:
            s += asi.price
        return s
