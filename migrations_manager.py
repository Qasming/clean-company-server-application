import os
import sys
import sqlite3

import config
from migrations import *

import migrations.sqlite as migrations


def migrate_all(db: sqlite3.Connection):
    migrations.CreateUserTableMigration(db).migrate()

    migrations.CreateServicesTableMigration(db).migrate()
    migrations.CreateServiceDetailsTableMigration(db).migrate()

    migrations.CreateAdditionalServicesTableMigration(db).migrate()
    migrations.CreateServiceAdditionalServicesTableMigration(db).migrate()

    migrations.CreateOrdersTableMigration(db).migrate()

    migrations.CreateOrderClientInfoTableMigration(db).migrate()

    migrations.CreateOrderPremisesInfoTableMigration(db).migrate()

    migrations.CreateOrderServiceInfoMigration(db).migrate()

    migrations.CreateOrderAdditionalServiceTableMigration(db).migrate()

    migrations.CreateReviewsTableMigration(db).migrate()


def rollback_all(db: sqlite3.Connection):
    migrations.CreateUserTableMigration(db).rollback()

    migrations.CreateServicesTableMigration(db).rollback()
    migrations.CreateServiceDetailsTableMigration(db).rollback()

    migrations.CreateAdditionalServicesTableMigration(db).rollback()
    migrations.CreateServiceAdditionalServicesTableMigration(db).rollback()

    migrations.CreateOrdersTableMigration(db).rollback()
    migrations.CreateOrderClientInfoTableMigration(db).rollback()
    migrations.CreateOrderAdditionalServiceTableMigration(db).rollback()

    migrations.CreateReviewsTableMigration(db).rollback()


if __name__ == '__main__':
    operation = (sys.argv[1])

    if operation == 'migrate':
        try:
            os.remove(config.DATABASE)
        except FileNotFoundError:
            pass

        os.system("sqlite3 ./" + config.DATABASE)

        db = sqlite3.connect(config.DATABASE)
        migrate_all(db)
        db.close()

    elif operation == 'rollback':
        db = sqlite3.connect(config.DATABASE)
        rollback_all(db)
        db.close()
