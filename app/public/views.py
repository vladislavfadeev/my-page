from flask import render_template, request, make_response, jsonify
import requests

from app.config import Config
from app.admin.models import (
    AboutMeModel,
    LocationContactModel,
    MyWorksModel,
    SocialContactModel,
)
from app.public import blueprint
from app.public.forms import FeedbackForm


@blueprint.route("/")
def index():
    info_items = AboutMeModel.query.all()
    works_items = MyWorksModel.query.all()
    location_items = LocationContactModel.query.all()
    social_items = SocialContactModel.query.all()
    works_attach_img = {}
    for i in works_items:
        works_attach_img[i.id] = i.attach_image.split(",")

    return render_template(
        "public/home.html",
        info_items=info_items,
        works_items=works_items,
        works_attach_img=works_attach_img,
        location_items=location_items,
        social_items=social_items,
    )


@blueprint.route("/feedback", methods=("POST",))
def feedbak():
    form = FeedbackForm(request.form)
    if form.validate():
        message = (
            "New message from vfadeev.dev!\n\n"
            f"u/a: {request.user_agent}\n"
            f"ip: {request.environ['HTTP_X_FORWARDED_FOR']}\n"
            f"name: {form.name.data}\n"
            f"contact: {form.contact.data}\n"
            f"message: {form.message.data}"
        )
        result = requests.get(
            f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}"
            f"/sendMessage?chat_id={Config.TG_USER_ID}&text={message}"
        )
        if result.status_code == 200:
            data = {'ok': True}
            return make_response(jsonify(data), 200)
    data = {'ok': False}
    return make_response(jsonify(data), 400)
