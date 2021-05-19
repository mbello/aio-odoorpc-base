"""The hypermodern Python project."""

try:
    from importlib.metadata import version, PackageNotFoundError  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore


try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"


from aio_odoorpc_base.helpers import odoo_base_url2jsonrpc_endpoint, \
                                     build_odoo_jsonrpc_endpoint_url, \
                                     execute_kwargs

from aio_odoorpc_base.aio import \
    about, \
    authenticate, \
    change_admin_password, \
    create_database, \
    db_exist, \
    drop_database, \
    dump_database, \
    duplicate_database, \
    execute_kw, \
    list_countries, \
    list_databases, \
    list_lang, \
    login, \
    migrate_databases, \
    rename_database, \
    restore_database, \
    server_version, \
    version
