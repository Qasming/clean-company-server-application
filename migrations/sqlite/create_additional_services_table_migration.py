from .migration import Migration


class CreateAdditionalServicesTableMigration(Migration):
    def migrate(self):
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE additional_services (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(30) NOT NULL,
            price INT NOT NULL
            )
        """)
        self.db.commit()
        cursor.close()

    def rollback(self):
        cursor = self.db.cursor()
        cursor.execute("DROP TABLE additional_services")
        self.db.commit()
        cursor.close()

