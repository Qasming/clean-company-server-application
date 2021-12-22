from abc import abstractmethod
from typing import List

from .models.review import Review


class ReviewRepository:
    @abstractmethod
    def get_last_reviews(self, count: int) -> List[Review]:
        pass

    @abstractmethod
    def get_review_by_order_id(self, order_id: int) -> Review:
        pass

    @abstractmethod
    def get_review_by_id(self, review_id: int) -> Review:
        pass

    @abstractmethod
    def save_review(self, review: Review):
        pass
