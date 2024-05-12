from archive.temp import db


class Words(db.Model):
    __tablename__ = "words"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4096))
    speach_part = db.Column(db.String(4096))
    translations = db.Column(db.String(4096))
    definition = db.Column(db.String(4096))
    importance = db.Column(db.Int())
    topic = db.Column(db.String(4096))