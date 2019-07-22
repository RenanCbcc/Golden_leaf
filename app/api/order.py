from flask import request

from app.api import api


@api.route('/order', methods=['POST'])
def save_order():
    print(request.data)

    # product = Product.from_json(request.json)
    # db.session.add(order)
    # db.session.commit()
    return request.json, 201, {'Location': "www.goldenleaf.com"}
