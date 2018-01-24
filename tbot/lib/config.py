"""Config file parsing for server information"""
import yaml


class ConfigParser:
    config_info = {}

    def __init__(self) -> None:
        """init to load project information and license info"""
        with open("config.yml", 'rb') as config_file:
            config_file_strings = config_file.read()
        self.config_info = yaml.load(config_file_strings)

    def get(self) -> dict:
        return self.config_info
