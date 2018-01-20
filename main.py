import random
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
subscribers_file = "subscribers.csv"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Subs:
    def __init__(self) -> None:
        """init"""
        with open(subscribers_file, 'r') as sub_file:
            self.sub_list = sub_file.readlines()

    @staticmethod
    def return_random_sub_name(sub_list) -> str:
        number_of_subs = len(sub_list)
        number_of_subs -= 1
        select_winner = random.randint(1, int(number_of_subs))
        name = sub_list[select_winner]
        return str(name[26:-1])


sub = Subs()
sub_name = sub.return_random_sub_name(sub.sub_list)
db.create_all()
check_for_user = User.query.filter_by(username=sub_name).first()


def check_user():
    if check_for_user is None:
        winning_sub = User(username=sub_name)
        db.session.add(winning_sub)
        db.session.commit()
        return sub_name


possible_sub_winner = check_user()
print(possible_sub_winner)
