"""odoo-cli-docker-compose entry point script."""

# odoo-cli-docker-compose/__main__.py


from tracker import cli, __app_name__

def main():
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()
