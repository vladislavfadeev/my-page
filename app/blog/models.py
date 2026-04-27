from datetime import datetime

from app.extensions import db


post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('blog_post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('blog_tag.id'), primary_key=True),
)


class BlogPost(db.Model):
    __tablename__ = 'blog_post'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    preview_text = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_published = db.Column(db.Boolean, default=False, nullable=False)
    views_count = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    tags = db.relationship('BlogTag', secondary=post_tags, backref='posts', lazy=True)
    reactions = db.relationship('PostReaction', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='post', lazy=True,
                               cascade='all, delete-orphan',
                               order_by='Comment.created_at.desc()')

    @property
    def likes_count(self):
        return self.reactions.filter_by(is_like=True).count()

    @property
    def dislikes_count(self):
        return self.reactions.filter_by(is_like=False).count()

    def user_reaction(self, user):
        if not user or not user.is_authenticated:
            return None
        r = self.reactions.filter_by(user_id=user.id).first()
        if r is None:
            return None
        return 'like' if r.is_like else 'dislike'

    def __str__(self):
        return self.title


class BlogTag(db.Model):
    __tablename__ = 'blog_tag'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(64), unique=True, nullable=False)
    slug = db.Column(db.String(64), unique=True, nullable=False)

    def __str__(self):
        return self.name


class PostReaction(db.Model):
    __tablename__ = 'post_reaction'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    is_like = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (db.UniqueConstraint('post_id', 'user_id', name='uq_post_reaction'),)


class Comment(db.Model):
    __tablename__ = 'blog_comment'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', backref='comments')

    def __str__(self):
        return f'Comment #{self.id}'
