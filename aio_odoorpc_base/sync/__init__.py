# ===== BASE METHODS =====
from aio_odoorpc_base.sync.rpc import \
    jsonrpc, \
    check_jsonrpc_response, \
    rpc_result, \
    rpc_call_and_check

# ===== OBJECT SERVICE =====
from aio_odoorpc_base.sync.object import execute_kw

# ===== COMMON SERVICE =====
from aio_odoorpc_base.sync.common import \
    about, \
    authenticate, \
    login, \
    version

# ===== DB SERVICE =====

# methods below require admin (super) password
from aio_odoorpc_base.sync.db import \
    change_admin_password, \
    create_database, \
    drop_database, \
    dump_database, \
    duplicate_database, \
    migrate_databases, \
    rename_database, \
    restore_database

# import aliases
# from aio_odoorpc_base.sync.db import \
#    drop, \
#    dump, \
#    rename, \
#    restore

# do not require admin (super) password
from aio_odoorpc_base.sync.db import \
    db_exist, \
    list_countries, \
    list_databases, \
    list_lang, \
    server_version
