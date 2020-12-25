"""
This script runs the Golden_Leaf application using a development server.
"""

from os import environ
from Golden_Leaf import create_app
from Golden_Leaf.settings import ProductionConfig, TestingConfig

app = create_app(ProductionConfig)

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT,True)
