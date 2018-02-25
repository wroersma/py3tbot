from app.auth.models import Group
from flask import session
from flask_login import current_user


def check_group(group_test):
    if session is not None:
        try:
            user_groups = session["groups"]
            if user_groups == group_test:
                return True
        except KeyError:
            return False


def get_groups():
    user_groups = Group.query.filter_by(username=current_user.username).first_or_404()
    session['groups'] = user_groups.group_name
    return session['groups']
