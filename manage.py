#!/usr/bin/env python3
from flask_migrate import MigrateCommand
from flask_script import Manager

from app import create_app, db, admin
from app.configuration.config import TestingConfig
from app.models.tables import Client, Clerk, Address, Product, Item, Order, Payment, AdminView

app = create_app(TestingConfig)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

admin.add_view(AdminView(Client, db.session))
admin.add_view(AdminView(Clerk, db.session))
admin.add_view(AdminView(Address, db.session))
admin.add_view(AdminView(Product, db.session))
admin.add_view(AdminView(Item, db.session))
admin.add_view(AdminView(Order, db.session))
admin.add_view(AdminView(Payment, db.session))


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade
    # migrate database to latest revision
    upgrade()


# To  create a migration folder type: Golden_leaf$ python3 manage.py db init
# To  perform a migration type: Golden_leaf$ python3 manage.py db migrate
# To  commit a migration type: Golden_leaf$ python3 manage.py db upgrade
# To get the application running type: Golden_leaf$ python3 manage.py runserver or even $gunicorn manage:app


if __name__ == '__main__':
    manager.run()
