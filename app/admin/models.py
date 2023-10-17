from app.extensions import db


class AboutMeModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(5000), nullable=False)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class MyWorksModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    title_image = db.Column(db.Text, unique=True, nullable=False)
    short_description = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    attach_image = db.Column(db.Text, unique=True, nullable=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title
    

class LocationContactModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(512), nullable=False)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class SocialContactModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    link = db.Column(db.String(2048), nullable=False)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title
