from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Plugin(db.Model):
    __tablename__ = "plugin"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    file_filename = db.Column(db.String(255))
    image_filename = db.Column(db.String(255))
