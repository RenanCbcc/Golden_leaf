#!/usr/bin/env python3
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app import create_app, db
from app.configuration.config import TestingConfig

app = create_app(TestingConfig)
migrate = Migrate(app, db)
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


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
