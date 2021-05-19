from typing import List, Optional, Union
from aio_odoorpc_base.protocols import T_HttpClient
from aio_odoorpc_base.sync.rpc import rpc_result
import base64

__SERVICE: str = 'db'

# Odoo's external API has no naming consistency for its 'db' methods.
# We have at the same time 'create_database' and 'duplicate_database', but then only 'drop' and 'dump'.
# I prefer the method names with '_database' because it better describes the method and provides
# naming consistency for the db methods.


def db_exist(http_client: T_HttpClient, url: str, *_,
             db_name: Optional[str] = None) -> bool:
    # support list unpacking used with model methods
    # [http_client, url: str, db: str, uid: int, password: str]
    # if _ has 3 items and the second is an int we can assume _[0] has the db_name
    db_name = _[0] if db_name is None and len(
        _) == 3 and isinstance(_[1], int) else db_name

    if db_name is None:
        raise RuntimeError("[db_exist] No database name provided.")

    return rpc_result(http_client, url, service=__SERVICE, method='db_exist',
                      args=[db_name], ensure_instance_of=bool)


def list_countries(http_client: T_HttpClient, url: str, master_password: str) -> List[str]:
    return rpc_result(http_client, url, service=__SERVICE, method='list_countries',
                      args=[master_password], ensure_instance_of=list)


def list_databases(http_client: T_HttpClient, url: str, *_,
                   document: Optional[bool] = None) -> List[str]:
    return rpc_result(http_client, url, service=__SERVICE, method='list',
                      args=None if document is None else [document],
                      ensure_instance_of=list)


def list_lang(http_client: T_HttpClient, url: str, *_) -> List[str]:
    return rpc_result(http_client, url, service=__SERVICE, method='list_lang',
                      ensure_instance_of=list)


def server_version(http_client: T_HttpClient, url: str, *_) -> str:
    return rpc_result(http_client, url, service=__SERVICE, method='server_version',
                      ensure_instance_of=str)


#  === DB MANAGEMENT METHODS: MAY BE DISABLED BY ODOO INSTANCE, ADMIN PASSWORD REQUIRED ===
# Functions below may or may not be allowed on the Odoo instance. Depends on a configuration
# to allow db management through the API.
def change_admin_password(http_client: T_HttpClient, url: str, master_password: str, *,
                          new_password: str) -> bool:
    # web/database/change_password / POST form-encoded / params master_pwd, master_pwd_new
    return rpc_result(http_client, url, service=__SERVICE, method="change_admin_password",
                      args=[master_password, new_password],
                      ensure_instance_of=bool)


def create_database(http_client: T_HttpClient, url: str, master_password: str, *,
                    db_name: str, demo: bool, lang: str, user_password: Optional[str] = None,
                    login: Optional[str] = None, country_code: Optional[str] = None,
                    phone: Optional[str] = None) -> bool:
    args: list = [master_password, db_name, demo, lang]
    opt_args: list = [user_password, login, country_code, phone]
    while len(opt_args) > 0 and opt_args[-1] is None:
        opt_args = opt_args[:-1]
    args.extend(opt_args)

    return rpc_result(http_client, url, service=__SERVICE, method="create_database",
                      args=args, ensure_instance_of=bool)


def drop_database(http_client: T_HttpClient, url: str, master_password: str, *,
                  db_name: str) -> bool:
    return rpc_result(http_client, url, service=__SERVICE, method="drop",
                      args=[master_password, db_name],
                      ensure_instance_of=bool)


def dump_database(http_client: T_HttpClient, url: str, master_password: str, *,
                  db_name: str, format: str = "zip") -> bytes:
    res = rpc_result(http_client, url, service=__SERVICE, method='dump',
                     args=[master_password, db_name, format], ensure_instance_of=str)
    return base64.b64decode(res)


def duplicate_database(http_client: T_HttpClient, url: str, master_password: str, *,
                       db_original_name: str, db_name: str) -> bool:
    return rpc_result(http_client, url, service=__SERVICE, method='duplicate_database',
                      args=[master_password, db_original_name, db_name], ensure_instance_of=bool)


def migrate_databases(http_client: T_HttpClient, url: str, master_password: str, *,
                      databases: List[str]) -> bool:
    return rpc_result(http_client, url, service=__SERVICE, method='migrate_databases',
                      args=[master_password, databases], ensure_instance_of=bool)


def rename_database(http_client: T_HttpClient, url: str, master_password: str, *,
                    old_name: str, new_name: str) -> bool:
    return rpc_result(http_client, url, service=__SERVICE, method='rename',
                      args=[master_password, old_name, new_name], ensure_instance_of=bool)


def restore_database(http_client: T_HttpClient, url: str, master_password: str, *,
                     db_name: str, data: Union[bytes, str], copy: bool = False) -> bool:
    # /web/database/restore / POST multipart/form-data / params: master_pwd, backup_file, name, copy
    if isinstance(data, bytes):
        data = base64.b64encode(data).decode('ascii')
    return rpc_result(http_client, url, service=__SERVICE, method='restore',
                      args=[master_password, db_name, data, copy], ensure_instance_of=bool)
