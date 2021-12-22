from .migration import Migration


class CreateServiceDetailsTableMigration(Migration):
    def migrate(self):
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE service_details (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            service_id INTEGER NOT NULL,
            title VARCHAR(30) NOT NULL,
            FOREIGN KEY(service_id) REFERENCES services(ID)
            );
        """)
        self.db.commit()
        cursor.close()

    def rollback(self):
        cursor = self.db.cursor()
        cursor.execute("""
            DROP TABLE service_details
        """)
        self.db.commit()
        cursor.close()
