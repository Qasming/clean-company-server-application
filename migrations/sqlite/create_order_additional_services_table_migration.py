from .migration import Migration


class CreateOrderAdditionalServiceTableMigration(Migration):
    def migrate(self):
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE order_additional_services (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                additional_service_id INTEGER NOT NULL,
                order_id INTEGER NOT NULL,
                price INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (additional_service_id) REFERENCES additional_services(ID),
                FOREIGN KEY (order_id) REFERENCES orders(ID)
            )
        """)
        self.db.commit()
        cursor.close()

    def rollback(self):
        cursor = self.db.cursor()
        cursor.execute("DROP TABLE order_additional_services")
        self.db.commit()
        cursor.close()
