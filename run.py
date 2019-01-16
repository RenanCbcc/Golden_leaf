from app import manager

# To  create a migration folder type: Golden_leaf$ python3 run.py db init
# To  perform a migration type: Golden_leaf$ python3 run.py db migrate
# To  commit a migration type: Golden_leaf$ python3 run.py db upgrade
# To get the application running type: Golden_leaf$ python3 run.py runserver

if __name__ == '__main__':
    manager.run()
