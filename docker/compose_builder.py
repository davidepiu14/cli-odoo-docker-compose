"""This module provides the ET expense model-controller."""

import datetime


from docker.database import DatabaseHandler
from docker import COMPOSE
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

import yaml



class CurrentOdooDockerImage(NamedTuple):
    image: Dict[str, Any]
    error: int


class OdooDockerComposeBuilder:

    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)
   
    def create_docker_compose(self, version):
        
        COMPOSE['services']['web'].update({
            'image': f'odoo:{version}'
        }) 
        write = self._db_handler.write_compose(COMPOSE)
        return CurrentOdooDockerImage(COMPOSE, write.error)
