import logging
import argparse
import os
from lib.logs import Logger
from lib.info import ProjectInfo
from lib.subscriber import return_random_sub_name, get_sub_list
from lib.database import User, check_user, db
from lib.config import get


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

    def run(self):
        if self.plugin == "giveaway":
            sub_list = get_sub_list(self.subscribers_file)
            sub_name = return_random_sub_name(sub_list)

            if os.path.exists(self.file_name) is True:
                # TODO clean this up to query user list before running it through the random picker
                check_for_user = User.query.filter_by(username=sub_name).first()
                possible_sub_winner = check_user(check_for_user, sub_name)
                logging.info("New winner inserted into DB " + str(possible_sub_winner))
                print("Congrats on winning " + possible_sub_winner)
            else:
                logging.info("No users found in db so adding the first one")
                db.create_all()
                check_for_user = None
                possible_sub_winner = check_user(check_for_user, sub_name)
                logging.info("New winner inserted into DB " + str(possible_sub_winner))
                # TODO return notification to the stream in some way
                print("Congrats on winning " + possible_sub_winner)
