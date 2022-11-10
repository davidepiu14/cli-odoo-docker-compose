
import yaml
from typer.testing import CliRunner
import pytest



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
    assert "%s v %s" % (__app_name__,__version__) in result.stdout


@pytest.fixture
def mock_yml_file(tmp_path):
    file = {
    "version": "3.1",
    "services":  {
        "web": 
            {
            "image": "odoo:14.0",
            "depends_on": ["db"],
            "ports": ["8069:8069", "8072:8072"],
            "volumes": [
                "./:/mnt/extra-addons", 
            ]
            },
        "db": 
            {
                "image": "postgres:13",
                "environment" : [
                    "POSTGRES_DB=postgres",
                    "POSTGRES_PASSWORD=odoo",
                    "POSTGRES_USER=odoo"
                ],
                "ports": ["5433:5432"]
            }
    }
}
    db_file = tmp_path / "docker-compose.test.json"
    with open("docker-compose.yml", mode="wt", encoding="utf-8") as file:
        yaml.dump(file, Dumper=MyDumper, default_flow_style=False) 
    return db_file



