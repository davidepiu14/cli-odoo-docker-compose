"""This module provides the cli-odoo-docker-compose database functionality."""

import configparser
import yaml
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from tracker import DB_WRITE_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS, DB_READ_ERROR

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
        "." + Path.home().stem + "docker-compose.yml"
)



def get_database_path(config_file: Path) -> Path:
    """Return the current path to the expense database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

def init_database(db_path: Path) -> int:
    """Create database."""
    try:
        db_path.write_text("") # Empty expense list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR


class MyDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


class DBResponse(NamedTuple):
    config_list: List[Dict[str, Any]]
    error: int


class DatabaseHandler:

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def write_compose(self, config_list: List[Dict[str, Any]]) -> DBResponse:
        try:
            #TODO
            with open("docker-compose.yml", mode="wt", encoding="utf-8") as file:
                yaml.dump(data,file, Dumper=OdooDockerComposeBuilder, default_flow_style=False) 
            
            return DBResponse(config_list, SUCCESS)

        except OSError: # Catch file IO problems
            return DBResponse(config_list, DB_WRITE_ERROR)



