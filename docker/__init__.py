"""Top-level package for odoo docker-container creation"""

__app_name__ = "cli-odoo-docker-container"
__version__ = "0.1.0"

(
        SUCCESS,
        DIR_ERROR,
        FILE_ERROR,
        DB_READ_ERROR,
        DB_WRITE_ERROR,
        JSON_ERROR,
        ID_ERROR,
) = range(7)

ERRORS = {
        DIR_ERROR: "config directory error",
        FILE_ERROR: "config file error",
}

COMPOSE = {
    "version": "3.1",
    "services":  {
        "web": 
            {
            "image": "odoo:%s.0",
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

