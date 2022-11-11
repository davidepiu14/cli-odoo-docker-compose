"""This module provides the cli-odoo-docker-compose model-controller."""
from odoo_docker.database import YmlHandler
from odoo_docker import COMPOSE
from pathlib import Path
from typing import Any, Dict, List, NamedTuple




class CurrentOdooDockerImage(NamedTuple):
    image: Dict[str, Any]
    error: int


class OdooDockerComposeBuilder:

    def __init__(self, yml_path: Path) -> None:
        self._db_handler = YmlHandler(yml_path)
   
    def create_docker_compose(self, version):
        
        COMPOSE['services']['web'].update({
            'image': f'odoo:{version}'
        }) 
        write = self._db_handler.write_compose(COMPOSE)
        return CurrentOdooDockerImage(COMPOSE, write.error)
