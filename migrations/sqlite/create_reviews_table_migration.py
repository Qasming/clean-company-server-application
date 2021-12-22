from .migration import Migration


class CreateReviewsTableMigration(Migration):
    def migrate(self):
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE reviews(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                text VARCHAR(255) NOT NULL,
                assessment INTEGER NOT NULL DEFAULT 1,
                date DATE NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(ID),
                FOREIGN KEY (user_id) REFERENCES users(ID)
            )
        """)
        self.db.commit()
        cursor.close()

    def rollback(self):
        cursor = self.db.cursor()
        cursor.execute("DROP TABLE reviews")
        self.db.commit()
        cursor.close()
