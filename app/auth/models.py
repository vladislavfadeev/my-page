from datetime import datetime

from werkzeug.security import generate_password_hash
from flask_login import UserMixin

from app.extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(255), nullable=False)
    hash_password = db.Column(db.String(255), nullable=True)

    provider = db.Column(db.String(32), nullable=True)
    provider_id = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    avatar_url = db.Column(db.String(500), nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (db.UniqueConstraint('provider', 'provider_id', name='uq_user_provider'),)

    @staticmethod
    def password_hasher(pswd: str):
        return generate_password_hash(pswd)

    @property
    def display_name(self):
        return self.username or self.email or f'user{self.id}'

    def __unicode__(self):
        return self.username

    def __str__(self):
        return self.username
