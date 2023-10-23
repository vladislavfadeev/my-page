from wtforms import form, fields, validators


class FeedbackForm(form.Form):
    name = fields.StringField(validators=[validators.Length(min=1, max=32)])
    contact = fields.StringField(validators=[validators.Length(min=1, max=64)])
    message = fields.TextAreaField(validators=[validators.Length(min=1, max=4096)])