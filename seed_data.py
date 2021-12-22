from infrastructure import sqlite_connection
import config
from seeders.services_seed import ServicesSeeder

if __name__ == '__main__':
    connection = sqlite_connection.SqliteConnection()
    connection.connect(config.DATABASE)
    seeder = ServicesSeeder(connection)
    seeder.seed()
    connection.close()
