from typing import overload, Literal, Mapping, Tuple, Union
from aio_odoorpc_base.protocols import T_HttpClient
from aio_odoorpc_base.sync.rpc import rpc_result


__SERVICE: str = 'common'


def login(http_client: T_HttpClient, url: str = '', *,
          db: str, login: str, password: str) -> Union[int, Literal[False]]:
    service, method = __SERVICE, 'login'
    args = [db, login, password]

    return rpc_result(http_client, url, service=service, method=method, args=args)


def authenticate(http_client: T_HttpClient, url: str = '', *,
                 db: str, login: str, password: str, user_agent_env: Mapping) -> Union[int, Literal[False]]:
    service, method = __SERVICE, 'authenticate'
    args = [db, login, password, user_agent_env]

    return rpc_result(http_client, url, service=service, method=method, args=args)


def version(http_client: T_HttpClient, url: str = '') -> str:
    service, method = __SERVICE, 'version'

    return rpc_result(http_client, url, service=service, method=method, ensure_instance_of=str)


@overload
def about(http_client: T_HttpClient, url: str, *, extended: Literal[False]) -> str:
    ...


@overload
def about(http_client: T_HttpClient, url: str, *, extended: Literal[True]) -> Tuple[str, str]:
    ...


def about(http_client, url='', *, extended):
    service, method = __SERVICE, 'about'
    args = [extended]

    return rpc_result(http_client, url, service=service, method=method, args=args)
