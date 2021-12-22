from .migration import Migration


class CreateOrdersTableMigration(Migration):
    def migrate(self):
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE orders (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INT NOT NULL,
            sum INT NOT NULL,
            status INTEGER DEFAULT 1,
            FOREIGN KEY(user_id) REFERENCES users(ID))
        """)
        self.db.commit()
        cursor.close()

    def rollback(self):
        cursor = self.db.cursor()
        cursor.execute("""
            DROP TABLE orders
        """)
        self.db.commit()
        cursor.close()
