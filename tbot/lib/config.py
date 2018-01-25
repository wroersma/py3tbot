"""Config file parsing for server information"""
import yaml
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def open_config(config) -> dict:
    with open(config, 'rb') as config_file:
        config_file_strings = config_file.read()
    config_info = yaml.load(config_file_strings)
    return config_info


def get(config) -> dict:
    config_info = open_config(config)
    return config_info


def get_default() -> iter:
    config = "tbot/config.yml"
    config_info = open_config(config)
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = config_info["config"]["SQLALCHEMY_DATABASE_URI"]
    db = SQLAlchemy(app)

    return config_info, app, db
