import logging
import os
from lib.info import ProjectInfo
from lib.subscriber import return_random_sub_name, get_sub_list
from lib.database import User, check_user, db

# TODO make a subscribers_file get from API function to check for an update every time we run
subscribers_file = "subscribers.csv"
file_name = "lib/tbot.db"


def main() -> None:
    """ Main Function to run py3tbot in a development ENV"""
    # create a basic logging level of info
    logging.basicConfig(level=logging.INFO)
    logging.info("Getting Project Info")
    # create a file handler
    handler = logging.FileHandler('py3tbot.log')
    handler.setLevel(logging.INFO)
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
    if os.path.exists(file_name) is True:
        check_for_user = User.query.filter_by(username=sub_name).first()
        possible_sub_winner = check_user(check_for_user, sub_name)
    else:
        logging.info("No users found in db so adding the first one")
        db.create_all()
        check_for_user = None
        possible_sub_winner = check_user(check_for_user, sub_name)
    print("Congrats on winning " + possible_sub_winner)


if __name__ == "__main__":
    main()
