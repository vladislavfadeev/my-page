import os
from pathlib import Path
import confuse


project_root = Path(__file__).resolve().parent.parent
os.environ['APPDIR'] = str(project_root)
appConfig = confuse.Configuration('APP')


class Config:
    TG_USER_ID = appConfig['feedback']['tg_id'].get()
    SECRET_KEY = appConfig['app']['secret'].get() or os.urandom(24)
    LANGUAGES = ['ru', 'en']    
    
    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(project_root, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOAD_DIR = f'{project_root}/app/static/works/img/'
    MANAGE_FILE_DIR = os.path.join(project_root, 'app/static')
    # MANAGE_FILE_DIR = os.path.join(os.path.dirname(__file__), 'static')


os.environ['ADMIN_USER_MODEL'] = 'User'
os.environ['ADMIN_USER_MODEL_USERNAME_FIELD'] = 'username'
os.environ['ADMIN_SECRET_KEY'] = appConfig['app']['secret'].get()