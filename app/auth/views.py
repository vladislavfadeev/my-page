from flask_classful import FlaskView, route
import flask_login as login
from flask_admin import helpers
from flask import request, redirect, url_for, render_template

from app.auth.forms import LoginForm

class LoginView(FlaskView):
    _form = LoginForm

    def get(self):
        if login.current_user.is_authenticated:
            return redirect(url_for('admin.index'))
        return render_template('auth/login.html', form=self._form())

    def post(self):
        form = self._form(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)
            return redirect(url_for('admin.index'))
        return render_template('auth/login.html', form=form)

    @login.login_required
    @route('logout')
    def logout(self):
        login.logout_user()
        return redirect(url_for('public.index'))