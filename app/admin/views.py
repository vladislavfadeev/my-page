import os
import flask_admin as admin
import flask_login as login
from flask import url_for, redirect, request
from flask_admin.contrib import sqla
from flask_admin.form import FormOpts
from flask_admin.contrib.fileadmin import FileAdmin
from werkzeug.utils import secure_filename
from pathlib import Path
import uuid

from app.admin.forms import (
    LocationContactForm,
    MyWorksCreateForm,
    MyWorksEditForm,
    AboutMeForm,
    SocialContactForm,
)
from app.config import Config
from app.extensions import db


class MyBaseModelView(sqla.ModelView):
    create_template = "admin/my_create.html"
    edit_template = "admin/my_edit.html"

    def is_accessible(self):
        return login.current_user.is_authenticated
    

class FileView(FileAdmin):
    def is_accessible(self):
        return login.current_user.is_authenticated


class MyWorksView(MyBaseModelView):
    def get_create_form(self):
        return MyWorksCreateForm

    def get_edit_form(self):
        return MyWorksEditForm

    @staticmethod
    def save_img(img, project_folder):
        upload_dir = Config.UPLOAD_DIR
        img_name = secure_filename(img.filename)
        Path(f"{upload_dir}/{project_folder}/").mkdir(parents=True, exist_ok=True)
        file_dir = f"{upload_dir}/{project_folder}/"
        img.save(os.path.join(file_dir, img_name))
        static_path = f"static/works/img/{project_folder}/{img_name}"
        return static_path

    @admin.expose("/new/", methods=("GET", "POST"))
    def create(self):
        return_url = self.get_url(".index_view")
        form = self.create_form()
        if request.method == "POST":
            if self.validate_form(form):
                project_folder = str(uuid.uuid4())[:4]
                title_image = self.save_img(form.title_image.data, project_folder)
                attach_images = ""
                for f in form.attach_image.data:
                    if f.filename != "":
                        attach_images += f",{self.save_img(f, project_folder)}"
                if attach_images.startswith(","):
                    attach_images = attach_images[1:]
                obj = self.model(
                    title=form.title.data,
                    title_image=title_image,
                    short_description=form.short_description.data,
                    description=form.description.data,
                    attach_image=attach_images,
                )
                db.session.add(obj)
                db.session.commit()

                if "_add_another" in request.form:
                    return redirect(request.url)
                elif "_continue_editing" in request.form:
                    return redirect(return_url)
                else:
                    return redirect(
                        self.get_save_return_url(self.model, is_created=True)
                    )

        form_opts = FormOpts(
            widget_args=self.form_widget_args, form_rules=self._form_create_rules
        )
        return self.render(
            self.create_template, form=form, form_opts=form_opts, return_url=return_url
        )


class AboutMeView(MyBaseModelView):
    form = AboutMeForm


class MyAdminIndexView(admin.AdminIndexView):
    @admin.expose("/")
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for("auth.LoginView:get"))
        return super(MyAdminIndexView, self).index()



class LocationModelView(MyBaseModelView):
    form = LocationContactForm


class SocialModelView(MyBaseModelView):
    form = SocialContactForm
