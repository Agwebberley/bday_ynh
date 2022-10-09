from flask import Flask
from flask_bootstrap import Bootstrap

def create_app():

    from .app import main

    app = Flask(__name__)
    app.register_blueprint(main)
    app.config['SECRET_KEY'] = 'mysecretkey'
    bootstrap = Bootstrap(app)




    return app
