from flask import Blueprint

blueprint = Blueprint('public', __name__,
                      url_prefix='',
                      static_folder='../static/public',
                      static_url_path='static/public')


from app.public import views