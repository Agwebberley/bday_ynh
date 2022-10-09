from flask import Flask


def create_app():

    from .app import main

    app = Flask(__name__)
    app.register_blueprint(main)



    return app
