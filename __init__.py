"""Top-level package for odoo docker-container creation"""
# expense/__init__.py

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
