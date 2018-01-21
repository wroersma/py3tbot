from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tbot.db'
db = SQLAlchemy(app)


class User(db.Model):
    db = SQLAlchemy(app)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


def check_user(check_for_user, sub_name):
    if check_for_user is None:
        winning_sub = User(username=sub_name)
        db.session.add(winning_sub)
        db.session.commit()
        return sub_name


