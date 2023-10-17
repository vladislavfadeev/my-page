from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager
from flask_ckeditor import CKEditor

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass



ckeditor = CKEditor()
babel = Babel()
db = SQLAlchemy(model_class=Base)
migrate = Migrate()
admin_panel = Admin(name='fva-web', template_mode='bootstrap4') #  base_template='my_master.html',
login_manager = LoginManager()