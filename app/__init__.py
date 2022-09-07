from dotenv import load_dotenv
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager

from .config import Config
from .auth import auth
from .models import UserModel

load_dotenv() # Take environment variables from .env

login_manager = LoginManager()
# Le decimos la ruta de login que maneje
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(username):
    return UserModel.query(username)

def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap5(app)
    
    app.config.from_object(Config)

    login_manager.init_app(app)

    app.register_blueprint(auth)

    return app