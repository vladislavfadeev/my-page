from flask import Blueprint

blueprint = Blueprint('blog', __name__,
                      url_prefix='/blog',
                      static_folder='../static/blog',
                      static_url_path='static/blog')


from app.blog import views
