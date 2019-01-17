from flask import redirect
from app import app


@app.errorhandler(404)
def page_not_found():
    return redirect('https://http.cat/{}'.format(404))


@app.errorhandler(500)
def internal_server_error():
    return redirect('https://http.cat/{}'.format(500))
