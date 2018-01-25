from config import get_default


# TODO Fix this trash and figure out how to not be so bad at coding
config_data = get_default()
db = config_data[2]


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


def add_winner(sub_name):
    winning_sub = User(username=sub_name)
    db.session.add(winning_sub)
    db.session.commit()
    return sub_name


