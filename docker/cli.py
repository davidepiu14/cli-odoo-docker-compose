import yaml
import typer

@app.command()
def create(
      	version: float = typer.Option(14.0, "--version", "-v"),
    ) -> None:
    """Create docker-compose.yml file with specified version"""
    docker_compose = create_docker_compose(version)
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

