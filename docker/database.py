"""This module provides the cli-odoo-docker-compose database functionality."""

import configparser
import yaml
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from docker import (
    DB_WRITE_ERROR, 
    DB_WRITE_ERROR, 
    SUCCESS, 
)

DEFAULT_DB_FILE_PATH = Path().resolve().joinpath("docker-compose.yml")


def get_database_path(config_file: Path) -> Path:
    """Return the current path to the expense database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

def init_database(db_path: Path) -> int:
    """Create database."""
    try:
        db_path.write_text("") 
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR


class DBResponse(NamedTuple):
    config_list: List[Dict[str, Any]]
    error: int


class DatabaseHandler(yaml.Dumper):


    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def increase_indent(self, flow=False, indentless=False):
        return super(DatabaseHandler, self).increase_indent(flow, False)
    
    def write_compose(self, config_list: List[Dict[str, Any]]) -> DBResponse:
        try:
            #TODO
            with open("docker-compose.yml", mode="wt", encoding="utf-8") as file:
                print(config_list)
                yaml.dump(config_list, file, Dumper=DatabaseHandler, default_flow_style=False) 
            return DBResponse(config_list, SUCCESS)

        except OSError: # Catch file IO problems
            return DBResponse(config_list, DB_WRITE_ERROR)



