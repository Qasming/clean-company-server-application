import datetime

from ...users.models.user import User
from ...orders.models.order import Order


class Review:
    id: int = 0
    user: User = None
    order: Order = None
    text: str
    assessment: int = 0
    date: datetime.date
