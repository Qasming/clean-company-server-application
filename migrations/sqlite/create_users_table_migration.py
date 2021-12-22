from .migration import Migration


class CreateUserTableMigration(Migration):
    def migrate(self):
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE users (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            phone VARCHAR(20) NOT NULL UNIQUE,
            first_name VARCHAR(30),
            last_name VARCHAR(30),
            middle_name VARCHAR(30),
            photo VARCHAR(255),
            email VARCHAR(30)
            )
        """)
        self.db.commit()
        cursor.close()

    def rollback(self):
        cursor = self.db.cursor()
        cursor.execute("""
        DROP TABLE users
        """)
        self.db.commit()
        cursor.close()
