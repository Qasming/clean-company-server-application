from .migration import Migration


class CreateOrderPremisesInfoTableMigration(Migration):
    def migrate(self):
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE order_premises_info (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            premises_type INTEGER NOT NULL,
            area INTEGER NOT NULL,
            address VARCHAR(255) NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(ID)
            )
        """)
        self.db.commit()
        cursor.close()

    def rollback(self):
        cursor = self.db.cursor()
        cursor.execute("""
            DROP TABLE order_premises_info
        """)
        self.db.commit()
        cursor.close()
