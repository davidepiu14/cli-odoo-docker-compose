"""This module provides the ET expense model-controller."""

import datetime

from pathlib import Path
from typing import Any, Dict, List, NamedTuple




class OdooDockerVersion:

    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def create_docker_compose(self, version):
        payload = 

        write = self._db_handler.write_compose(version)
        return CurrentDockerVersion(payload, write.error)
