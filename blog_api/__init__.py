from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from blog_api.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
# api = Api()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    from blog_api.apis import blueprint as api

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(api)
    return app