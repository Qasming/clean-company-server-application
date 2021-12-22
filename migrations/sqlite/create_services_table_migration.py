from .migration import Migration


class CreateServicesTableMigration(Migration):
    def migrate(self):
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE services (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            price INT NOT NULL,
            description VARCHAR(255)
            )
        """)
        self.db.commit()
        cursor.close()

    def rollback(self):
        cursor = self.db.cursor()
        cursor.execute("DROP TABLE services")
        self.db.commit()
        cursor.close()

