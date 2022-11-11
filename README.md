# cli-odoo-docker-compose


Set-up your locally enviroment to work with Odoo and docker, no more copy and past from other projects


## Roadmap

- [ ] Set-up repository if needed

- [x] Select Odoo version

- [ ] Select in which port to expose Odoo

- [ ] Select or create the directory to mount

- [ ] Postgres dumps and restore 

## Installation
1. ```pip3 install -r requirements.txt```
2. ``` python3 -m venv venv```
3. ``` . venv/bin/activate```

## Usage 
```Usage: cli-odoo-docker-container [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version                   Show the application's version and exit.
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  create  Create docker-compose.yml file with specified version
  init    Initialize docker-compose.yml file
  ```
  
  ## Example
  
  - ```python3 -m odoo_docker init```
  - ```python3 -m odoo_docker create -v 12.0```
  
  This will results in: 
  ```
  services:
  db:
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_PASSWORD=odoo
      - POSTGRES_USER=odoo
    image: postgres:13
    ports:
      - 5433:5432
  web:
    depends_on:
      - db
    image: odoo:12.0
    ports:
      - 8069:8069
      - 8072:8072
    volumes:
      - ./:/mnt/extra-addons
version: '3.1'
```
