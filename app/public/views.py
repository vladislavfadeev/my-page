from flask import render_template

from flask import render_template
from app.admin.models import AboutMeModel, LocationContactModel, MyWorksModel, SocialContactModel
from app.public import blueprint


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
