from flask_classful import FlaskView, route
import flask_login as login
from flask_admin import helpers
from flask import request, redirect, url_for, render_template, session

from app.extensions import db
from app.auth.forms import LoginForm, RegisterForm
from app.auth.models import User
from app.auth import oauth, captcha
from app.config import Config


def _safe_next(default_endpoint):
    nxt = request.args.get('next') or request.form.get('next')
    if nxt and nxt.startswith('/'):
        return nxt
    return url_for(default_endpoint)


class LoginView(FlaskView):
    _form = LoginForm

    def get(self):
        if login.current_user.is_authenticated:
            return redirect(_safe_next('admin.index' if login.current_user.is_admin else 'blog.index'))
        return self._render(self._form())

    def post(self):
        form = self._form(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)
            return redirect(_safe_next('admin.index' if user.is_admin else 'blog.index'))
        return self._render(form)

    def _render(self, form):
        return render_template(
            'auth/login.html',
            form=form,
            oauth_config=Config.OAUTH,
            tg_bot_username=Config.TG_BOT_USERNAME,
            next_url=request.args.get('next', ''),
        )

    @login.login_required
    @route('logout')
    def logout(self):
        login.logout_user()
        return redirect(url_for('public.index'))


def register():
    if login.current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = RegisterForm(request.form) if request.method == 'POST' else RegisterForm()
    if request.method == 'POST':
        valid = form.validate()
        captcha_ok = captcha.check(form.captcha.data)
        if not captcha_ok:
            form.captcha.errors = list(form.captcha.errors) + ['Неверный код с картинки']
        if valid and captcha_ok:
            user = User(
                username=form.username.data.strip(),
                email=form.email.data.strip(),
                hash_password=User.password_hasher(form.password.data),
            )
            db.session.add(user)
            db.session.commit()
            login.login_user(user)
            return redirect(_safe_next('blog.index'))

    return render_template(
        'auth/register.html',
        form=form,
        captcha_svg=captcha.generate(),
        next_url=request.args.get('next', ''),
    )


def register_routes(blueprint):
    blueprint.add_url_rule(
        '/auth/login/<provider>',
        view_func=oauth.start,
        endpoint='oauth_start',
    )
    blueprint.add_url_rule(
        '/auth/callback/<provider>',
        view_func=oauth.callback,
        endpoint='oauth_callback',
    )
    blueprint.add_url_rule(
        '/auth/telegram',
        view_func=oauth.telegram_callback,
        endpoint='oauth_telegram',
    )
    blueprint.add_url_rule(
        '/auth/register',
        view_func=register,
        endpoint='register',
        methods=['GET', 'POST'],
    )
