import re

from wtforms import form, fields, validators
from werkzeug.security import check_password_hash

from app.extensions import db
from app.auth.models import User


EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


class LoginForm(form.Form):
    login = fields.StringField('Login или email', validators=[validators.InputRequired()])
    password = fields.PasswordField('Пароль', validators=[validators.InputRequired()])

    def validate_login(self, field):
        user = self.get_user()
        if user is None:
            raise validators.ValidationError('Invalid user')
        if not user.hash_password or not check_password_hash(user.hash_password, self.password.data):
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return (db.session.query(User)
                .filter(db.or_(User.username == self.login.data, User.email == self.login.data),
                        User.hash_password.isnot(None))
                .first())


class RegisterForm(form.Form):
    username = fields.StringField('Имя', validators=[
        validators.InputRequired(),
        validators.Length(min=2, max=64),
    ])
    email = fields.StringField('Email', validators=[validators.InputRequired()])
    password = fields.PasswordField('Пароль', validators=[
        validators.InputRequired(),
        validators.Length(min=6, max=128),
    ])
    password_confirm = fields.PasswordField('Повторите пароль', validators=[
        validators.InputRequired(),
        validators.EqualTo('password', message='Пароли не совпадают'),
    ])
    captcha = fields.StringField('Код с картинки', validators=[validators.InputRequired()])

    def validate_email(self, field):
        if not EMAIL_RE.match(field.data or ''):
            raise validators.ValidationError('Некорректный email')
        if db.session.query(User).filter_by(email=field.data).first():
            raise validators.ValidationError('Email уже зарегистрирован')

    def validate_username(self, field):
        exists = (db.session.query(User)
                  .filter_by(username=field.data, provider=None)
                  .first())
        if exists:
            raise validators.ValidationError('Имя уже занято')
