from app.auth.models import Group
from flask import session
from flask_login import current_user


def get_groups():
    user_groups = Group.query.filter_by(username=current_user.username).first_or_404()
    if user_groups.group_name == "admin":
        session['groups'] = user_groups.group_name
        return session['groups']
    else:
        return session


def check_group(group_test):
    if session is not None:
        try:
            if group_test == session["groups"]:
                return True
        except KeyError:
            return False


