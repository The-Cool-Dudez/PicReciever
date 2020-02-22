from app.db import db

class Images(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    path = db.Column(db.String(5000), unique=True, nullable=False)

    def __init__(self, path):
        self.path = path
