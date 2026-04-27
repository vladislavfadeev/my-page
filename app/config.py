import os
from pathlib import Path
import confuse


project_root = Path(__file__).resolve().parent.parent
os.environ['APPDIR'] = str(project_root)
appConfig = confuse.Configuration('APP')


def _oauth(provider):
    try:
        return {
            'client_id': appConfig['oauth'][provider]['client_id'].get() or None,
            'client_secret': appConfig['oauth'][provider]['client_secret'].get() or None,
        }
    except confuse.NotFoundError:
        return {'client_id': None, 'client_secret': None}


def _opt(*path, default=None):
    try:
        return appConfig[path[0]][path[1]].get() if len(path) == 2 else appConfig[path[0]].get()
    except confuse.NotFoundError:
        return default


class Config:
    TG_USER_ID = appConfig['feedback']['tg_id'].get()
    TG_BOT_TOKEN = appConfig['feedback']['bot_token'].get()
    TG_BOT_USERNAME = _opt('oauth', 'telegram_bot_username', default=None)
    TG_AUTH_BOT_TOKEN = _opt('oauth', 'telegram_bot_token', default=None)
    SECRET_KEY = appConfig['app']['secret'].get() or os.urandom(24)
    LANGUAGES = ['ru', 'en']

    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(project_root, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_DIR = f'{project_root}/app/static/works/img/'
    MANAGE_FILE_DIR = os.path.join(project_root, 'app/static')

    OAUTH = {
        'google': _oauth('google'),
        'github': _oauth('github'),
    }


os.environ['ADMIN_USER_MODEL'] = 'User'
os.environ['ADMIN_USER_MODEL_USERNAME_FIELD'] = 'username'
os.environ['ADMIN_SECRET_KEY'] = appConfig['app']['secret'].get()
