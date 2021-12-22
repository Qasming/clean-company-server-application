from .migration import Migration


class CreateOrderServiceInfoMigration(Migration):
    def migrate(self):
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE order_service_info (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                service_id INTEGER NOT NULL,
                service_price INTEGER NOT NULL,
                FOREIGN KEY(order_id) REFERENCES orders(ID),
                FOREIGN KEY(service_id) REFERENCES services(ID)
            )
        """)
        self.db.commit()
        cursor.close()

    def rollback(self):
        cursor = self.db.cursor()
        cursor.execute("DROP TABLE order_service_info")
        self.db.commit()
        cursor.close()
