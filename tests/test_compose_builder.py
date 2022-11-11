import yaml
import logging
from typer.testing import CliRunner
import pytest

_logger = logging.getLogger(__name__)


from docker import (
    DB_READ_ERROR,
    SUCCESS,
    __app_name__,
    __version__,
    cli,
    compose_builder,
)


runner = CliRunner()


class MyDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert "%s v %s" % (__app_name__, __version__) in result.stdout


@pytest.fixture
def mock_yml_file(tmp_path):
    file = {
        "version": "3.1",
        "services": {
            "web": {
                "image": "odoo:14.0",
                "depends_on": ["db"],
                "ports": ["8069:8069", "8072:8072"],
                "volumes": [
                    "./:/mnt/extra-addons",
                ],
            },
            "db": {
                "image": "postgres:13",
                "environment": [
                    "POSTGRES_DB=postgres",
                    "POSTGRES_PASSWORD=odoo",
                    "POSTGRES_USER=odoo",
                ],
                "ports": ["5433:5432"],
            },
        },
    }
    db_file = "docker-compose.yml"
    with open(db_file, mode="wt", encoding="utf-8") as db:
        yaml.dump(file, db, Dumper=MyDumper, default_flow_style=False) 

    return db_file



test_data1 =  {
        "version": "3.1",
        "services": {
            "web": {
                "image": "odoo:14.0",
                "depends_on": ["db"],
                "ports": ["8069:8069", "8072:8072"],
                "volumes": [
                    "./:/mnt/extra-addons",
                ],
            },
            "db": {
                "image": "postgres:13",
                "environment": [
                    "POSTGRES_DB=postgres",
                    "POSTGRES_PASSWORD=odoo",
                    "POSTGRES_USER=odoo",
                ],
                "ports": ["5433:5432"],
            },
        },
    }

test_data2 =  {
        "version": "3.1",
        "services": {
            "web": {
                "image": "odoo:13.0",
                "depends_on": ["db"],
                "ports": ["8069:8069", "8072:8072"],
                "volumes": [
                    "./:/mnt/extra-addons",
                ],
            },
            "db": {
                "image": "postgres:13",
                "environment": [
                    "POSTGRES_DB=postgres",
                    "POSTGRES_PASSWORD=odoo",
                    "POSTGRES_USER=odoo",
                ],
                "ports": ["5433:5432"],
            },
        },
    }

@pytest.mark.parametrize(
        "version, expected",
        [
            pytest.param(
                '14.0',
                (test_data1, SUCCESS)
            ),
            pytest.param(
                '13.0',
                (test_data2, SUCCESS)
            )
        ]
)

def test_create_docker_compose(mock_yml_file, version, expected):
    docker_compose = compose_builder.OdooDockerComposeBuilder(mock_yml_file)
    assert docker_compose.create_docker_compose(version) == expected
