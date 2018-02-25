from flask import session


def check_group(group_test):
    if session is not None:
        try:
            user_groups = session["groups"]
            if user_groups == group_test:
                return True
        except KeyError:
            return False
