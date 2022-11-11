import yaml
import typer
import datetime

from pathlib import Path
from typing import List, Optional


from odoo_docker import (
        ERRORS, 
        __app_name__, 
        __version__, 
        config, 
        database,
        compose_builder
)

app = typer.Typer()


@app.command()
def init(
        db_path: str = typer.Option(
            str(database.DEFAULT_DB_FILE_PATH),
            "--db-path",
            "-db",
            prompt="docker-compose.yml location",
        ),
) -> None:
    """Initialize docker-compose.yml file"""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
                "Creating config file failed with %s" % (ERRORS[app_init_error]),
        fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
                "Creating databse failed with %s" % (ERRORS[db_init_error]),
                fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else: 
        typer.secho(
                f"The expense database is {db_path}",
                fg=typer.colors.GREEN
        )

def _version_callback(value: bool) -> None:
    if value: 
        typer.echo(f"{__app_name__} v {__version__}")
        raise typer.Exit()


@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the application's version and exit.",
            callback=_version_callback,
            is_eager=True,
        )
) -> None:
    return

def get_docker_compose() -> compose_builder.OdooDockerComposeBuilder:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
                'Config file not found. Please, run "docker init"',
                fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return compose_builder.OdooDockerComposeBuilder(db_path)

@app.command()
def create(
      	version: float = typer.Option(14.0, "--version", "-v"),
    ) -> None:
    """Create docker-compose.yml file with specified version"""
    docker = get_docker_compose()
    docker_compose, error = docker.create_docker_compose(version)
    if error:
        typer.secho(
                'Docker-compose creation failed with %s' % (ERRORS[error]),
                fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else: 
        typer.secho(
            f"""expense: "Docker-compose.yml created """
            f"""for version: {version}""",
            fg=typer.colors.GREEN,
        )

