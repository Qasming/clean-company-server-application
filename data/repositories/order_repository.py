from typing import List

from business.orders.models.order import Order
from business.orders.models.additional_service_info import AdditionalServiceInfo
from business.orders.models.client_info import ClientInfo
from business.orders.models.service_info import ServiceInfo
from business.orders.models.premises_info import PremisesInfo
from business.services.models.service import Service
from business.services.models.additional_service import AdditionalService
from business.orders.order_repository import OrderRepository as OrderRepositoryInterface
from business.orders.exceptions import OrderNotFound
from business.users.user_respository import UserRepository

from .sqlite_repository import SqliteRepository
from .services_repository import ServicesRepository
from .sqlite_repository import SqliteConnection


class OrderRepository(SqliteRepository, OrderRepositoryInterface):
    def __init__(self,
                 service_repository: ServicesRepository,
                 user_repository: UserRepository,
                 db: SqliteConnection):
        super(OrderRepository, self).__init__(db)
        self._service_repository = service_repository
        self._user_repository = user_repository

    def get_user_orders(self, user_id: int) -> List[Order]:
        orders: List[Order] = []
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM orders WHERE user_id = :user_id", {
            'user_id': user_id
        })
        rows = cursor.fetchall()
        for row in rows:
            order_id = int(row['ID'])
            order = self.get_order(order_id)
            orders.append(order)
        return orders

    def get_order(self, order_id: int) -> Order:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM orders WHERE ID = :order_id", {
            'order_id': order_id
        })
        rows = cursor.fetchall()
        if len(rows) == 0:
            raise OrderNotFound()
        row = rows[0]
        cursor.close()

        order = Order()

        order.id = int(row['ID'])

        status = None
        if int(row['status']) == 1:
            status = Order.Status.PENDING
        elif int(row['status']) == 2:
            status = Order.Status.COMPLETED
        elif int(row['status']) == 3:
            status = Order.Status.CANCELED

        order.status = status

        order.client_info = ClientInfo()
        client_info_row = self.__get_order_client_info(order.id)
        order.client_info.phone = client_info_row['phone']
        order.client_info.first_name = client_info_row['first_name']
        order.client_info.last_name = client_info_row['last_name']
        order.client_info.middle_name = client_info_row['middle_name']

        order.service_info = ServiceInfo()
        service_info_row = self.__get_order_service_info(order.id)
        order.service_info.service = self._service_repository.get_service_by_id(int(service_info_row['service_id']))
        order.service_info.service_price = (int(service_info_row['service_price']))

        order.premises_info = PremisesInfo()
        premises_info_row = self.__get_order_premises_info(order.id)

        premises_type = None
        if int(premises_info_row['premises_type']) == 1:
            premises_type = PremisesInfo.PremisesType.FLAT
        elif int(premises_info_row['premises_type']) == 2:
            premises_type = PremisesInfo.PremisesType.OFFICE
        elif int(premises_info_row['premises_type']) == 3:
            premises_type = PremisesInfo.PremisesType.HOUSE

        order.premises_info.premises_type = premises_type
        order.premises_info.area = int(premises_info_row['area'])
        order.premises_info.address = premises_info_row['address']

        order.additional_services = self.__get_order_additional_services(order.id)

        return order

    def save(self, order: Order) -> Order:
        if order.id == 0:
            return self.__insert_order(order)
        else:
            return self.__update_order(order)

    def remove(self, order: Order) -> Order:
        pass

    def __insert_order(self, order: Order) -> Order:
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO orders (
            user_id, sum, status
            ) VALUES ( 
                :user_id,
                :sum,
                :status
            )
        """, {
            'user_id': order.user.id,
            'sum': order.sum,
            'status': int(order.status.value)
        })
        self.db.commit()
        cursor.execute("""
        SELECT * FROM orders WHERE id=(SELECT max(id) FROM orders)
        """)
        row = cursor.fetchall()[0]
        order_id: int = int(row['ID'])
        self.__save_order_service_info(order_id, order.service_info)
        self.__save_order_client_info(order_id, order.client_info)
        self.__save_order_premises_info(order_id, order.premises_info)
        self.__save_order_additional_services(order_id, order.additional_services)
        return self.get_order(order_id)

    def __update_order(self, order: Order) -> Order:
        cursor = self.db.cursor()
        cursor.execute("""
                UPDATE orders
                SET
                status = :status
                WHERE ID = :order_id
                """, {
            'order_id': order.id,
            'status': int(order.status.value)
        })
        self.db.commit()
        return self.get_order(order.id)

    def __save_order_service_info(self, order_id: int, service_info: ServiceInfo):
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO order_service_info (
                order_id,
                service_id,
                service_price
            ) VALUES (
                :order_id,
                :service_id,
                :service_price
            )
        """, {
            'order_id': order_id,
            'service_id': service_info.service.id,
            'service_price': service_info.service.price
        })
        self.db.commit()
        cursor.close()

    def __save_order_premises_info(self, order_id: int, premises_info: PremisesInfo):
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO order_premises_info (
                order_id,
                premises_type,
                area,
                address
            ) VALUES (
                :order_id,
                :premises_type,
                :area,
                :address
            )
        """, {
            'order_id': order_id,
            'premises_type': premises_info.premises_type,
            'area': premises_info.area,
            'address': premises_info.address
        })
        self.db.commit()
        cursor.close()

    def __save_order_client_info(self, order_id: int, client_info: ClientInfo):
        cursor = self.db.cursor()
        cursor.execute("""
                    INSERT INTO order_client_info (
                        order_id,
                        first_name,
                        last_name,
                        middle_name,
                        phone
                    ) VALUES (
                        :order_id,
                        :first_name,
                        :last_name,
                        :middle_name,
                        :phone
                    )
                """, {
            'order_id': order_id,
            'first_name': client_info.first_name,
            'last_name': client_info.last_name,
            'middle_name': client_info.middle_name,
            'phone': client_info.phone
        })
        self.db.commit()
        cursor.close()

    def __get_order_client_info(self, order_id) -> dict:
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM order_client_info WHERE order_id = :order_id', {
            'order_id': order_id
        })
        return cursor.fetchall()[0]

    def __get_order_service_info(self, order_id) -> dict:
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM order_service_info WHERE order_id = :order_id', {
            'order_id': order_id
        })
        return cursor.fetchall()[0]

    def __get_order_premises_info(self, order_id) -> dict:
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM order_premises_info WHERE order_id = :order_id', {
            'order_id': order_id
        })
        return cursor.fetchall()[0]

    def __save_order_additional_services(self, order_id, additional_services_info: List[AdditionalServiceInfo]):
        cursor = self.db.cursor()
        for service_info in additional_services_info:
            cursor.execute("""
                INSERT INTO order_additional_services (
                    order_id,
                    additional_service_id,
                    price
                ) VALUES (
                    :order_id,
                    :additional_service_id,
                    :price
                )
            """, {
                'order_id': order_id,
                'additional_service_id': service_info.service.id,
                'price': service_info.price
            })
            self.db.commit()
        cursor.close()

    def __get_order_additional_services(self, order_id: int) -> List[AdditionalServiceInfo]:
        additional_services_info: List[AdditionalServiceInfo] = []

        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM order_additional_services WHERE order_id = :order_id", {
            'order_id': order_id
        })

        rows = cursor.fetchall()

        for row in rows:
            service_id = int(row['additional_service_id'])
            additional_service: AdditionalService = self._service_repository.get_additional_service_by_id(service_id)
            additional_service_info: AdditionalServiceInfo = AdditionalServiceInfo()
            additional_service_info.service = additional_service
            additional_service_info.price = int(row['price'])
            additional_services_info.append(additional_service_info)

        return additional_services_info
