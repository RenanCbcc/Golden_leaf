from flask_script import Manager
from app import create_app, db
from flask_migrate import Migrate, MigrateCommand
from app.configuration.config import TestingConfig

app = create_app(TestingConfig)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# To  create a migration folder type: Golden_leaf$ python3 run.py db init
# To  perform a migration type: Golden_leaf$ python3 run.py db migrate
# To  commit a migration type: Golden_leaf$ python3 run.py db upgrade
# To get the application running type: Golden_leaf$ python3 run.py runserver


if __name__ == '__main__':
    manager.run()
