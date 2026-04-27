from flask import Flask

from app.public import blueprint as public_bp
from app.auth import blueprint as login_bp
from app.blog import blueprint as blog_bp
from app.config import Config
from app.extensions import db, babel, migrate, admin_panel, login_manager, ckeditor
from app.auth.models import User
from app.admin.models import (
    LocationContactModel,
    MyWorksModel,
    AboutMeModel,
    SocialContactModel,
)
from app.admin.views import (
    AboutMeView,
    FileView,
    LocationModelView,
    MyWorksView,
    MyAdminIndexView,
    SocialModelView,
)
from app.blog.models import BlogPost, BlogTag, Comment
from app.blog.admin import BlogPostView, BlogTagView, CommentView


# @babel.localeselector
# def get_locale():
#     if request.args.get('lang'):
#         session['lang'] = request.args.get('lang')
#     elif not session.get('lang'):
#         session['lang'] = request.accept_languages.best_match(current_app.config['LANGUAGES'])
#     return session.get('lang', 'ru')


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    admin_panel._set_admin_index_view(index_view=MyAdminIndexView())
    admin_panel.add_view(
        FileView(Config.MANAGE_FILE_DIR, "/static/", name="Files")
    )
    admin_panel.add_view(AboutMeView(AboutMeModel, db.session, name='About me'))
    admin_panel.add_view(MyWorksView(MyWorksModel, db.session, name='My works'))
    admin_panel.add_view(LocationModelView(LocationContactModel, db.session, name='My location'))
    admin_panel.add_view(SocialModelView(SocialContactModel, db.session, name='My socials'))
    admin_panel.add_view(BlogPostView(BlogPost, db.session, name='Blog Posts', category='Blog'))
    admin_panel.add_view(BlogTagView(BlogTag, db.session, name='Blog Tags', category='Blog'))
    admin_panel.add_view(CommentView(Comment, db.session, name='Blog Comments', category='Blog'))

    db.init_app(app)
    babel.init_app(app)
    migrate.init_app(app, db)
    ckeditor.init_app(app)
    login_manager.init_app(app)
    admin_panel.init_app(app)

    login_manager.login_view = 'auth.LoginView:get'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

    app.register_blueprint(public_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(blog_bp)

    return app
