import datetime
from typing import List

from business.reviews.models.review import Review
from business.reviews.review_repository import ReviewRepository as ReviewRepositoryInterface
from business.reviews.exceptions.review_not_found import ReviewNotFound
from business.users.user_respository import UserRepository
from business.orders.order_repository import OrderRepository
from .sqlite_repository import SqliteRepository, SqliteConnection


class ReviewRepository(SqliteRepository, ReviewRepositoryInterface):
    def __init__(self,
                 user_repository: UserRepository,
                 order_repository: OrderRepository,
                 db: SqliteConnection):
        super(ReviewRepository, self).__init__(db)
        self._user_repository = user_repository
        self._order_repository = order_repository

    def get_last_reviews(self, count: int) -> List[Review]:
        reviews: List[Review] = []
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM reviews ORDER BY ID DESC LIMIT :count",{'count': count})
        rows = cursor.fetchall()
        for row in rows:
            user_id = row['user_id']
            order_id = row['order_id']
            user = self._user_repository.find_user_by_id(user_id)
            order = self._order_repository.get_order(order_id)
            review = Review()
            review.id = int(row['ID'])
            review.user = user
            review.order = order
            review.date = None
            review.text = row['text']
            review.assessment = int(row['assessment'])
            reviews.append(review)
        cursor.close()
        return reviews

    def get_review_by_order_id(self, order_id: int) -> Review:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM reviews WHERE order_id =:order_id", {
            "order_id": order_id
        })
        rows = cursor.fetchall()
        if len(rows) == 0:
            raise ReviewNotFound()
        row = rows[0]
        user_id = row['user_id']
        order_id = row['order_id']
        user = self._user_repository.find_user_by_id(user_id)
        order = self._order_repository.get_order(order_id)
        review = Review()
        review.id = int(row['ID'])
        review.user = user
        review.order = order
        review.date = None
        review.text = row['text']
        review.assessment = int(row['assessment'])
        return review

    def get_review_by_id(self, review_id: int) -> Review:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM reviews WHERE ID =:review_id", {
            "review_id": review_id
        })
        rows = cursor.fetchall()
        if len(rows) == 0:
            raise ReviewNotFound()
        row = rows[0]
        user_id = row['user_id']
        order_id = row['order_id']
        user = self._user_repository.find_user_by_id(user_id)
        order = self._order_repository.get_order(order_id)
        review = Review()
        review.id = int(row['ID'])
        review.user = user
        review.order = order
        review.date = None
        review.text = row['text']
        review.assessment = int(row['assessment'])
        return review

    def save_review(self, review: Review) -> Review:
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO reviews (user_id, order_id, text, assessment)
            VALUES(:user_id, :order_id, :text, :assessment
        """, {
            "user_id": review.user.id,
            "order_id": review.order.id,
            "text": review.text,
            "assessment": review.assessment
        })
        self.db.commit()
        cursor.execute("SELECT * FROM reviews ORDER BY ID DESC LIMIT 1")
        row = cursor.fetchall()[0]
        user_id = row['user_id']
        order_id = row['order_id']
        user = self._user_repository.find_user_by_id(user_id)
        order = self._order_repository.get_order(order_id)
        review = Review()
        review.id = int(row['ID'])
        review.user = user
        review.order = order
        review.date = None
        review.text = row['text']
        review.assessment = int(row['assessment'])
        return review
