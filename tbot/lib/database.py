import datetime
from config import get_default
from flask import Flask

# TODO Fix this trash and figure out how to not be so bad at coding
config_data = get_default("tbot/config.yml")
db = config_data[2]


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128))
    website = db.Column(db.String(128))
    affiliation = db.Column(db.String(128))
    country = db.Column(db.String(32))
    bracket = db.Column(db.String(32))
    banned = db.Column(db.Boolean, default=False)
    verified = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)
    joined = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username


def add_winner(sub_name):
    winning_sub = User(username=sub_name)
    db.session.add(winning_sub)
    db.session.commit()
    return sub_name


def create_admin_user():
    app = Flask(__name__)
    # TODO clean this up to get from config file as it's just a placeholder right
    app.config['MYSQL_DATABASE_USER'] = 'jay'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'jay'
    app.config['MYSQL_DATABASE_DB'] = 'BucketList'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'