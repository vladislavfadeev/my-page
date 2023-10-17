from flask import Blueprint
from app.auth import views

blueprint = Blueprint('auth', __name__,
                      url_prefix='',
                      static_folder='../static/auth',
                      static_url_path='static/auth')


views.LoginView.register(blueprint)