import typer

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
        yml_path: str = typer.Option(
            str(database.DEFAULT_DB_FILE_PATH),
            "--db-path",
            "-db",
            prompt="docker-compose.yml location",
        ),
) -> None:
    """Initialize docker-compose.yml file"""
    app_init_error = config.init_app(yml_path)
    if app_init_error:
        typer.secho(
                "Creating docker-compose.yml failed with %s" % (ERRORS[app_init_error]),
        fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_yml(Path(yml_path))
    if db_init_error:
        typer.secho(
                "[ODOO-DOCKER-COMPOSE] Creating docker-compose.yml failed with %s" % (ERRORS[db_init_error]),
                fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else: 
        typer.secho(
                f"[ODOO-DOCKER-COMPOSE] The docker-compose file is {yml_path}",
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

def get_docker_compose_builder() -> compose_builder.OdooDockerComposeBuilder:
    if config.CONFIG_FILE_PATH.exists():
        yml_path = database.get_yml_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
                'Config file not found. Please, run "docker init"',
                fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if yml_path.exists():
        return compose_builder.OdooDockerComposeBuilder(yml_path)

@app.command()
def create(
      	version: float = typer.Option(14.0, "--version", "-v"),
    ) -> None:
    """Create docker-compose.yml file with specified version"""
    compose_builder = get_docker_compose_builder()
    docker_compose, error = compose_builder.create_docker_compose(version)
    if error:
        typer.secho(
                '[ODOO-DOCKER-COMPOSE] Docker-compose creation failed with %s' % (ERRORS[error]),
                fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else: 
        typer.secho(
            f"""[ODOO-DOCKER-COMPOSE] "docker-compose.yml created """
            f"""for version: {version}""",
            fg=typer.colors.GREEN,
        )

