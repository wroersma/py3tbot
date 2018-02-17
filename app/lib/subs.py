import random
from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_babel import _, lazy_gettext as _l


def get_subscribers_file():
    """"""
    # TODO make a subscribers_file get from API function to check for an update every time we run
    print("this is a place holder for a future function")


def get_sub_list(subscribers_file) -> list:
    """get_subscribers_file"""
    with open(subscribers_file, 'r') as sub_file:
        sub_list = sub_file.readlines()
        return sub_list


def get_user_name_list(sub_list) -> list:
    user_list = []
    for item in sub_list:
        user_list.append(item[26:-1])
    user_list.remove('')
    return user_list


def get_non_winning_sub_list(sub_user_name_list, winner_list) -> list:
    non_winning_sub_list = []
    string_user_name_winner_list = []
    for item in winner_list:
        user_name = item.username
        if item != user_name:
            string_user_name_winner_list.append(user_name)
    for user_name_item in sub_user_name_list:
        if user_name_item not in string_user_name_winner_list:
            non_winning_sub_list.append(user_name_item)
    return non_winning_sub_list


def return_random_sub_name(sub_user_name_list):
    number_of_subs = len(sub_user_name_list)
    if number_of_subs > 0:
        select_winner = random.randint(0, int(number_of_subs - 1))
        name = sub_user_name_list[select_winner]
        return str(name)
    else:
        flash(u'There are not more valid winner with the selected options', 'error')
        name = None
        return name


class DrawWinner(FlaskForm):
    Product = StringField(_l('Product'), validators=[DataRequired()])
    submit = SubmitField(_l('Draw a winner'))

