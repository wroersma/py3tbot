import logging
import argparse
import os
import ujson
from lib.logs import Logger
from lib.info import ProjectInfo
from lib.subscriber import return_random_sub_name, get_sub_list, get_user_name_list, get_non_winning_sub_list
from lib.database import User, db, add_winner, create_admin_user
from lib.config import get
from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
conn = db


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/showsignup')
def showsignup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        user_info = {}
        if _name and _email and _password:
            _hashed_password = generate_password_hash(_password)
            user_info["username"] = _name
            user_info["email"] = _email
            user_info["password"] = _hashed_password
            create_admin_user(user_info)
            return ujson.dumps({'message': 'User created successfully !'})
    finally:
        conn.close()


class Py3TBOT:
    """Main Class for Py3TBOT App"""
    def __init__(self) -> None:
        args = self.parse_args()
        self.default_logging = Logger()
        Logger.default_logging()
        self.plugin = args.plugin
        self.config_file = args.config
        config_data = get(self.config_file)
        self.subscribers_file = config_data["config"]["subscribers_file"]
        self.file_name = config_data["config"]["file_name"]

        run = ProjectInfo()
        project_data = run.get()
        self.project_info_data = project_data["info"]
        self.project_version_data = project_data["version"]

        # Nice Formatting Suggestion from iofault
        self.__version__ = "%(major)s.%(minor)s.%(revision)s" % self.project_version_data

        for items in self.project_info_data:
            logging.info(str(items) + ":" + str(self.project_info_data[items]))
        logging.info(self.__version__)

    @staticmethod
    def parse_args() -> iter:
        parser_args = argparse.ArgumentParser(description="Welcome to the py3tbot jungle")
        parser_args.add_argument("-p", "--plugin", help="The plugin you want to run example: giveaway")
        parser_args.add_argument("-c", "--config", help="The config.yml file for the bot", default="tbot/config.yml")
        args = parser_args.parse_args()
        return args

    @app.route("/tbot")
    def run(self):
        if self.plugin == "giveaway":
            sub_list = get_sub_list(self.subscribers_file)
            winner_list = User.query.order_by(User.username).all()
            sub_user_name_list = get_user_name_list(sub_list)
            non_winning_sub_list = get_non_winning_sub_list(sub_user_name_list, winner_list)
            sub_name = return_random_sub_name(non_winning_sub_list)

            if os.path.exists(self.file_name) is False:
                logging.info("No users found in db so adding the first one")
                db.create_all()

            add_winner(sub_name)
            logging.info("New winner inserted into DB " + str(sub_name))
            print("Congrats on winning " + sub_name)

    def create_app(self):
        config_data = get(self.config_file)
        app.config['SQLALCHEMY_DATABASE_URI'] = config_data["config"]["SQLALCHEMY_DATABASE_URI"]
        db.init_app(app)
        return app
