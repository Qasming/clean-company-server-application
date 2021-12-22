from .migration import Migration


class CreateServiceAdditionalServicesTableMigration(Migration):
    def migrate(self):
        cursor = self.db.cursor()
        cursor.execute("""
        CREATE TABLE service_additional_services (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            service_id INT NOT NULL,
            additional_service_id INT NOT NULL,
            FOREIGN KEY(service_id) REFERENCES services(ID),
            FOREIGN KEY(additional_service_id) REFERENCES additional_services(ID)
        );
        """)
        self.db.commit()
        cursor.close()

    def rollback(self):
        cursor = self.db.cursor()
        cursor.execute("DROP TABLE service_additional_service")
        self.db.commit()
        cursor.close()

