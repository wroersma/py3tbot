import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from lib.info import ProjectInfo
from lib.subscriber import return_random_sub_name, get_sub_list
from lib.database import User, check_user
subscribers_file = "subscribers.csv"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tbot.db'
db = SQLAlchemy(app)


def main() -> None:
    """ Main Function to run py3tbot in a development ENV"""
    logging.basicConfig(level=logging.INFO)
    logging.info("Getting Project Info")
    run = ProjectInfo()
    project_data = run.get()
    project_info_data = project_data["info"]
    project_version_data = project_data["version"]
    # Nice Formatting Suggestion from iofault
    __version__ = "%(major)s.%(minor)s.%(revision)s" % project_version_data
    for items in project_info_data:
        logging.info(str(items) + ":" + str(project_info_data[items]))
    logging.info(__version__)
    sub_list = get_sub_list(subscribers_file)
    sub_name = return_random_sub_name(sub_list)
    db.create_all()
    check_for_user = User.query.filter_by(username=sub_name).first()
    possible_sub_winner = check_user(check_for_user, sub_name)
    print(possible_sub_winner)


if __name__ == "__main__":
    main()






