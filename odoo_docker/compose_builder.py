"""This module provides the cli-odoo-docker-compose model-controller."""
import git

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
        self.compose = COMPOSE
   
    def create_docker_compose(self, version) -> CurrentOdooDockerImage:
        self.compose.update({
            'image': f'odoo:{version}'
        }) 
        write = self._db_handler.write_compose(self.compose)
        return CurrentOdooDockerImage(self.compose, write.error)
    
    def set_up_repository(self) -> None:
        return git.Repo.init()



    

