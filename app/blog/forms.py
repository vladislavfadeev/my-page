from wtforms import form, fields, validators


class CommentForm(form.Form):
    content = fields.TextAreaField(
        'Комментарий',
        validators=[validators.InputRequired(), validators.Length(min=2, max=2000)],
    )
