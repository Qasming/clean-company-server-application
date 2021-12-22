from .migration import Migration


class CreateOrderClientInfoTableMigration(Migration):
    def migrate(self):
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE order_client_info (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            first_name VARCHAR(30) NOT NULL,
            last_name VARCHAR(30) NOT NULL,
            middle_name VARCHAR(30),
            phone VARCHAR(20) NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(ID)
            )
        """)
        self.db.commit()
        cursor.close()

    def rollback(self):
        cursor = self.db.cursor()
        cursor.execute("""
            DROP TABLE order_client_info
        """)
        self.db.commit()
        cursor.close()
