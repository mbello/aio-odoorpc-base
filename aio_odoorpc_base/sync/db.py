from typing import List
from aio_odoorpc_base.protocols import T_HttpClient
from aio_odoorpc_base.sync.rpc import rpc_result


__SERVICE: str = 'db'


def db_exist(http_client: T_HttpClient, url: str = '', *, db_name: str) -> bool:
    service, method = __SERVICE, 'db_exist'
    args = [db_name]

    return rpc_result(http_client, url, service=service, method=method, args=args, ensure_instance_of=bool)


# no Alias for list as it can cause issues overriding the 'list' python class
def list_databases(http_client: T_HttpClient, url: str = '', *, document: bool = False) -> List[str]:
    service, method = __SERVICE, 'list'
    args = [document]

    return rpc_result(http_client, url, service=service, method=method, args=args, ensure_instance_of=bool)


def list_lang(http_client: T_HttpClient, url: str = '') -> List[str]:
    service, method = __SERVICE, 'list_lang'

    return rpc_result(http_client, url, service=service, method=method, ensure_instance_of=list)


def list_countries(http_client: T_HttpClient, url: str = '') -> List[str]:
    service, method = __SERVICE, 'list_countries'

    return rpc_result(http_client, url, service=service, method=method, ensure_instance_of=list)


def server_version(http_client: T_HttpClient, url: str = '') -> str:
    service, method = __SERVICE, 'server_version'

    return rpc_result(http_client, url, service=service, method=method, ensure_instance_of=str)


#  === DB MANAGEMENT METHODS: MAY BE DISABLED BY ODOO INSTANCE, ADMIN PASSWORD REQUIRED ===
# Functions below may or may ot be allowed on the Odoo instance. Depends on a configuration
# to allow db management through the API.


def create_database(http_client: T_HttpClient, url: str = '', *, admin_password: str,
                    db_name: str, demo: bool, lang: str, user_password: str = 'admin',
                    login: str = 'admin', country_code: str = None, phone: str = None) -> bool:
    service, method = __SERVICE, 'create_database'
    args = [admin_password, db_name, demo, lang,
            user_password, login, country_code, phone]

    return rpc_result(http_client, url, service=service, method=method, args=args, ensure_instance_of=bool)


def duplicate_database(http_client: T_HttpClient, url: str = '', *, admin_password: str,
                       db_original_name: str, db_name: str) -> bool:
    service, method = __SERVICE, 'duplicate_database'
    args = [admin_password, db_original_name, db_name]

    return rpc_result(http_client, url, service=service, method=method, args=args, ensure_instance_of=bool)


def drop_database(http_client: T_HttpClient, url: str = '', *, admin_password: str,
                  db_name: str) -> bool:
    service, method = __SERVICE, 'drop'
    args = [admin_password, db_name]

    return rpc_result(http_client, url, service=service, method=method, args=args, ensure_instance_of=bool)


def dump_database(http_client: T_HttpClient, url: str = '', *, admin_password: str,
                  db_name: str, format: str = "zip") -> bytes:
    service, method = __SERVICE, 'dump'
    args = [admin_password, db_name, format]

    res = rpc_result(http_client, url, service=service,
                     method=method, args=args, ensure_instance_of=str)
    return res.encode()


def restore_database(http_client: T_HttpClient, url: str = '', *, admin_password: str,
                     db_name: str, data: bytes, copy: bool = False) -> bool:
    service, method = __SERVICE, 'restore'
    args = [admin_password, db_name, data, copy]

    return rpc_result(http_client, url, service=service, method=method, args=args, ensure_instance_of=bool)


def rename_database(http_client: T_HttpClient, url: str = '', *, admin_password: str,
                    old_name: str, new_name: str) -> bool:
    service, method = __SERVICE, 'rename'
    args = [admin_password, old_name, new_name]

    return rpc_result(http_client, url, service=service, method=method, args=args, ensure_instance_of=bool)


def migrate_databases(http_client: T_HttpClient, url: str = '', *, admin_password: str,
                      databases: List[str]) -> bool:
    service = __SERVICE
    method = 'migrate_databases'
    args = [admin_password, databases]

    return rpc_result(http_client, url, service=service, method=method, args=args, ensure_instance_of=bool)


def change_admin_password(http_client: T_HttpClient, url: str = '', *, admin_password: str,
                          new_password: str) -> bool:
    service, method = __SERVICE, 'change_admin_password'
    args = [admin_password, new_password]

    return rpc_result(http_client, url, service=service, method=method, args=args, ensure_instance_of=bool)


# Odoo's external API is not consistent on the naming of its db methods.
# We have at the same time 'create_database' and 'duplicate_database', but then only 'drop' and 'dump'.
# I prefer the method names with '_database' because it better describes the method.
# But for those expecting an exact mirror of Odoo's external APIs, we have some aliases for the methods
# that do not follow the '_database' naming pattern.
# drop = drop_database
# dump = dump_database
# restore = restore_database
# rename = rename_database
