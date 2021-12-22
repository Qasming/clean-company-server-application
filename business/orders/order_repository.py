from abc import abstractmethod
from typing import List

from .models.order import Order


class OrderRepository:
    @abstractmethod
    def get_user_orders(self, user_id: int) -> List[Order]:
        pass

    @abstractmethod
    def get_order(self, order_id: int) -> Order:
        pass

    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    @abstractmethod
    def remove(self, order: Order) -> Order:
        pass
