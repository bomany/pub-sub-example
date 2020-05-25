import os

from flask import Flask, render_template
from flask_socketio import SocketIO

from .consumer import MessagingAPI


def start_messaging_api():
    return MessagingAPI(
        user='rabbitmq',
        password='rabbitmq',
        url='rabbitmq',
        topic='flask_topic'
    )


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app


app = create_app()
socketio = SocketIO(app)


def emit_message(ch, method, properties, body):
    if isinstance(body, bytes):
        body = body.decode('utf-8')

    socketio.emit('new message', {'data': body}, namespace='/')


messaging_api = start_messaging_api()
messaging_api.start_consumer(queue='shared_consumer', callback=emit_message)


@app.route('/')
def home():
    return render_template('index.html')


@socketio.on('send_message')
def send_message(message):
    if isinstance(message, dict):
        message = message.get('data', '')

    messaging_api.send_message(message)
