"""This module provides the ET expense model-controller."""

import datetime


from database import DatabaseHandler

from pathlib import Path
from typing import Any, Dict, List, NamedTuple



class CurrentOdooDockerImage(NamedTuple):
    image: Dict[str, Any]
    error: int


class OdooDockerComposeBuilder:

    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def create_docker_compose(self, version, port):
        payload = """
       %s %s""" % (version, port)
        write = self._db_handler.write_compose(version)
        return CurrentOdooDockerImage(payload, write.error)
