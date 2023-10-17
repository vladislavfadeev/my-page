from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from app.extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(255), nullable=False)
    hash_password = db.Column(db.String(255), nullable=False)

    @staticmethod
    def password_hasher(pswd: str):
        return generate_password_hash(pswd)

    def __unicode__(self):
        return self.username

    def __str__(self):
        return self.username
