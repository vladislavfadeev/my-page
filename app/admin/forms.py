from wtforms import form, fields, validators
from flask_ckeditor import CKEditorField


class MyWorksCreateForm(form.Form):
    title = fields.StringField(validators=[validators.InputRequired()])
    title_image = fields.FileField(validators=[validators.InputRequired()])
    short_description = CKEditorField(validators=[validators.InputRequired()])
    description = CKEditorField(validators=[validators.InputRequired()])
    attach_image = fields.MultipleFileField()


class MyWorksEditForm(MyWorksCreateForm):
    title_image = fields.StringField(validators=[validators.InputRequired()])
    attach_image = fields.StringField(validators=[validators.InputRequired()])
    

class AboutMeForm(form.Form):
    title = fields.StringField(validators=[validators.InputRequired()])
    description = CKEditorField(validators=[validators.InputRequired()])


class LocationContactForm(form.Form):
    title = fields.StringField(validators=[validators.InputRequired()])
    location = CKEditorField(validators=[validators.InputRequired()])


class SocialContactForm(form.Form):
    title = fields.StringField(validators=[validators.InputRequired()])
    link = CKEditorField(validators=[validators.InputRequired()])