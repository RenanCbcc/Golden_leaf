from app import create_app
from app.settings import ProductionConfig

app = create_app(ProductionConfig)
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)


# To  create a migration folder type: Golden_leaf$ python3 wsgi.py db init
# To  perform a migration type: Golden_leaf$ python3 wsgi.py db migrate
# To  commit a migration type: Golden_leaf$ python3 wsgi.py db upgrade
# To get the application running type: Golden_leaf$ python3 wsgi.py runserver or even $gunicorn manage:app

if __name__ == '__main__':
    app.run(debug=True)
