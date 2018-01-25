import logging
from tbot.lib.logs import Logger
from tbot.py3tbot import Py3TBOT


def main() -> None:
    """ CLI tool for running py3tbot"""
    Logger.default_logging()
    logging.basicConfig(filename="tbot.log", filemode='w', level=logging.INFO)
    tbot = Py3TBOT()
    tbot.parse_args()
    tbot.run()


if __name__ == "__main__":
    main()
