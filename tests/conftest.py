import pytest
from typing import Any, Callable, Tuple
from aio_odoorpc_base.sync.common import login
from aio_odoorpc_base.protocols import T_HttpClient
import httpx


@pytest.fixture(scope='session')
def runbot_url_db_user_pwd(runbot_url_db_user_pwd) -> Tuple[str, str, str, str]:
    base_url, url_jsonrpc, db, username, password = runbot_url_db_user_pwd
    return url_jsonrpc, db, username, password


@pytest.fixture(scope='session')
def known_master_pwd_url_masterpwd(runbot_url_db_user_pwd) -> Tuple[str, str]:
    # Add manually the info for an Odoo instance with known master password.
    # Usually the OCA Runbot runs its instances with no Master Password set.
    # Must visit https://runbot.odoo-community.org/runbot, find a running instance,
    # Copy its URL below, and then access /web/database/manager and set the password to
    # 'admin' or to whatever we return last/second in the tuple below
    return 'http://3475626-11-0-0b1a90.runbot1.odoo-community.org/jsonrpc', 'admin'


@pytest.fixture(scope='session')
def base_args_common(runbot_url_db_user_pwd) -> Callable[[Any], Tuple[Any, str, str, str, str]]:
    url, db, username, pwd = runbot_url_db_user_pwd
    
    def func(client):
        return client, url, db, username, pwd
    return func


@pytest.fixture(scope='session')
def base_args_obj(runbot_url_db_user_pwd) -> Callable[[Any], Tuple[Any, str, str, int, str]]:
    url, db, username, pwd = runbot_url_db_user_pwd
    with httpx.Client() as http_client:
        uid = login(http_client=http_client, url=url, db=db, login=username, password=pwd)
    
    def func(client):
        return client, url, db, uid, pwd
    return func


@pytest.fixture(scope='session')
def base_args_db_no_masterpwd(runbot_url_db_user_pwd) -> Callable[[Any], Tuple[Any, str]]:
    url = runbot_url_db_user_pwd[0]
    
    def func(client):
        return client, url
    return func


@pytest.fixture(scope='session')
def base_args_db_with_masterpwd(known_master_pwd_url_masterpwd) -> Callable[[Any], Tuple[Any, str, str]]:
    url, master_pwd = known_master_pwd_url_masterpwd
    
    def func(client):
        return client, url, master_pwd
    return func


@pytest.fixture(scope='session')
def base_args_common(runbot_url_db_user_pwd) -> Callable[[Any], Tuple[Any, str, str, str, str]]:
    url, db, username, password = runbot_url_db_user_pwd
    
    def func(client):
        return client, url, db, username, password
    return func


@pytest.fixture(scope='session')
def version() -> str:
    return '14.0'


@pytest.fixture(scope='session')
def http_client() -> str:
    with httpx.Client() as client:
        yield client
