from controllers.auth_controller import AuthController
from controllers.services_controller import ServiceController
from controllers.user_controller import UserController
from controllers.order_controller import OrderController

from business.users.user_service import UserService
from business.services.services_service import ServicesService

from business.auth.code_service import CodeService
from business.auth.auth_service import AuthService

from business.orders.order_service import OrderService

from data.repositories.services_repository import ServicesRepository as SqliteServicesRepository
from data.repositories.user_repository import UserRepository as SqliteUserRepository
from data.auth.code_store import CodeStore
from data.auth.code_repository import CodeRepository
from data.repositories.order_repository import OrderRepository as SqliteOrderRepository
from data.repositories.review_repository import ReviewRepository as SqliteReviewRepository
from infrastructure.sqlite_connection import SqliteConnection

from config import DATABASE


class Application:
    def __init__(self):
        self._code_store = CodeStore()

        self._database = SqliteConnection()

        self._database.connect(DATABASE)

        self._user_repository = SqliteUserRepository(self._database)

        self._service_repository = SqliteServicesRepository(self._database)

        self._order_repository = SqliteOrderRepository(
            self._service_repository,
            self._user_repository,
            self._database)

        self._code_repository = CodeRepository(self._code_store)

        self._review_repository = SqliteReviewRepository(
            self._user_repository,
            self._order_repository,
            self._database
        )

        self._user_service = UserService(self._user_repository)

        self._services_service = ServicesService(self._service_repository)

        self._code_service = CodeService(self._code_repository)

        self._order_service = OrderService(
            self._order_repository,
            self._services_service,
            self._user_service
        )

        self._auth_service = AuthService(
            code_service=self._code_service,
            user_service=self._user_service
        )

    def __del__(self):
        self._database.close()

    @property
    def auth(self) -> AuthController:
        return AuthController(self._auth_service,
                              self._user_service
        )

    @property
    def services(self) -> ServiceController:
        return ServiceController(self._services_service)

    @property
    def users(self) -> UserController:
        return UserController(self._user_service)

    @property
    def orders(self) -> OrderController:
        return OrderController(self._order_service)
