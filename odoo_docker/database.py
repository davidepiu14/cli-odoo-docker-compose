"""This module provides the cli-odoo-docker-compose .yml handler functionality."""

import configparser
import yaml
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from odoo_docker import (
    DB_WRITE_ERROR, 
    DB_WRITE_ERROR, 
    SUCCESS, 
)

DEFAULT_DB_FILE_PATH = Path().resolve().joinpath("docker-compose.yml")


def get_yml_path(config_file: Path) -> Path:
    """Return the current path to the expense database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

def init_yml(yml_path: Path) -> int:
    """Create .yml file"""
    try:
        yml_path.write_text("") 
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR


class YmlResponse(NamedTuple):
    config_list: List[Dict[str, Any]]
    error: int


class MyDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)

class YmlHandler:

    def __init__(self, yml_path: Path) -> None:
        self._yml_path = yml_path
    
    def write_compose(self, config_list: List[Dict[str, Any]]) -> YmlResponse:
        try:
            with open("docker-compose.yml", mode="wt", encoding="utf-8") as file:
                yaml.dump(config_list, file, Dumper=MyDumper, default_flow_style=False) 
            return YmlResponse(config_list, SUCCESS)

        except OSError: # Catch file IO problems
            return YmlResponse(config_list, DB_WRITE_ERROR)



