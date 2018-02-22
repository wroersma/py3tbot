import logging
import os
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import db
from app.main.forms import EditProfileForm, SearchForm, MessageForm
from app.models import User, Message, Notification, Award, Group
from app.main import bp
from app.lib.subs import get_sub_list, get_non_winning_sub_list, get_user_name_list, return_random_sub_name, DrawWinner


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # page = request.args.get('page', 1, type=int)
    return render_template('index.html', title=_('Home'))


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    # page = request.args.get('page', 1, type=int)
    return render_template('user.html', user=user)


@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_popup.html', user=user)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'), form=form)


@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user, body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash(_('Your message has been sent.'))
        return redirect(url_for('main.user', username=recipient))
    return render_template('send_message.html', title=_('Send Message'), form=form, recipient=recipient)


@bp.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(Message.timestamp.desc()).paginate(
               page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.messages', page=messages.next_num) if messages.has_next else None
    prev_url = url_for('main.messages', page=messages.prev_num) if messages.has_prev else None
    return render_template('messages.html', messages=messages.items, next_url=next_url, prev_url=prev_url)


@bp.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{'name': n.name, 'data': n.get_data(), 'timestamp': n.timestamp} for n in notifications])


def add_winner(sub_name, project_name):
    winning_sub = Award(username=sub_name, award_name=project_name)
    db.session.add(winning_sub)
    db.session.commit()
    return sub_name


@bp.route('/groups')
@login_required
def groups():
    group_info = Group.query.order_by(Group.group_name).all()
    return render_template('groups.html', group_info=group_info)


@bp.route('/giveaway', methods=['GET', 'POST'])
@login_required
def giveaway():
    form = DrawWinner()
    if form.Product.data is not None and len(form.Product.data) > 0:
        # TODO fix this so it's a config option or stored in the database from an api call
        subscribers_file = "subscribers.csv"
        sub_list = get_sub_list(subscribers_file)
        winner_list = Award.query.order_by(Award.username).all()
        sub_user_name_list = get_user_name_list(sub_list)
        non_winning_sub_list = get_non_winning_sub_list(sub_user_name_list, winner_list)
        sub_name = return_random_sub_name(non_winning_sub_list)
        if sub_name is not None:
            add_winner(sub_name, form.Product.data)
            logging.info("New winner inserted into DB " + str(sub_name))
            flash(_('Congrats on winning ' + str(form.Product.data) + " " + sub_name + " !"))
        winning_sub_list = Award.query.order_by(Award.username).all()
        return render_template('giveaway.html', form=form, winning_sub_list=winning_sub_list)
    elif form.validate_on_submit() is False:
        winning_sub_list = Award.query.order_by(Award.username).all()
        return render_template('giveaway.html', form=form, winning_sub_list=winning_sub_list)
