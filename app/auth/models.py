from datetime import datetime
from app import db


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(128), index=True)
    username = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Group {}>'.format(self.group_name)
