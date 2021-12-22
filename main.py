from flask import Flask, request, render_template
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from config import JWT_SECRET_KEY, DEBUG_MODE
from application import Application
from werkzeug.routing import BaseConverter
import waitress

app: Application = Application()

flask = Flask(__name__)
flask.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY  # Change this!
jwt = JWTManager(flask)



@flask.route('/api/auth/get_code', methods=['POST'])
@cross_origin(supports_credentials=True)
def auth_get_code():
    if request.method == 'POST':
        return app.auth.get_code(request)


@flask.route('/api/auth/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def auth_login():
    if request.method == 'POST':
        return app.auth.login(request)


@flask.route('/api/auth/me', methods=['GET'])
@cross_origin(supports_credentials=True)
@jwt_required()
def get_me():
    return app.auth.me()


@flask.route('/api/users', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_users():
    return app.users.get_all()


@flask.route('/api/users/<index>', methods=['PUT'])
@cross_origin(supports_credentials=True)
@jwt_required()
def update_user():
    return app.users.update_user(request)


@flask.route('/api/users/<index>', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_users_one(index):
    return app.users.get_one(int(index))


@flask.route('/api/services', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_services():
    return app.services.get_all_services()


@flask.route('/api/services/<index>', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_service_by_id(index):
    return app.services.get_service_by_id(int(index))


@flask.route('/api/services/<index>/additional_services', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_service_additional_services(index):
    return app.services.get_service_additional_services(int(index))


@flask.route('/api/orders', methods=['POST'])
@cross_origin(supports_credentials=True)
@jwt_required()
def create_order():
    return app.orders.create_order(request)

@flask.route('/api/orders', methods=['GET'])
@cross_origin(supports_credentials=True)
@jwt_required()
def get_orders():
    return app.orders.get_user_orders()

@flask.route('/api/orders/<order_id>', methods=['GET'])
@cross_origin(supports_credentials=True)
@jwt_required()
def get_order(order_id):
    return app.orders.get_order(int(order_id))


@flask.route('/api/orders/<order_id>', methods=['PUT'])
@cross_origin(supports_credentials=True)
@jwt_required()
def update_order(order_id):
    if str(request.json['action']) == 'complete':
        return app.orders.complete_order(int(order_id))
    elif str(request.json['action']) == 'cancel':
        return app.orders.cancel_order(int(order_id))


@flask.route('/js/<file>')
def static_js(file):
    return flask.send_static_file("js/" + file)


@flask.route('/css/<file>')
def static_css(file):
    return flask.send_static_file("css/" + file)


@flask.route('/img/<file>')
def static_img(file):
    return flask.send_static_file("img/" + file)


@flask.route('/', defaults={'path': ''})
@flask.route('/<path:path>')
def catch_all(path):
    return flask.send_static_file("index.html")


if __name__ == '__main__':
    flask.debug = DEBUG_MODE
    # flask.run()
    from waitress import serve
    serve(flask, host="0.0.0.0", port=5000)
