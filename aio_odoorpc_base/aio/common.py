from typing import overload, Literal, Mapping, Tuple, Union
from aio_odoorpc_base.protocols import T_AsyncHttpClient
from aio_odoorpc_base.aio.rpc import rpc_result


__SERVICE: str = 'common'


async def login(http_client: T_AsyncHttpClient, url: str = '', *,
                db: str, login: str, password: str) -> Union[int, Literal[False]]:
    service, method = __SERVICE, 'login'
    args = [db, login, password]

    return await rpc_result(http_client, url, service=service, method=method, args=args)


async def authenticate(http_client: T_AsyncHttpClient, url: str = '', *,
                       db: str, login: str, password: str, user_agent_env: Mapping) -> Union[int, Literal[False]]:
    service, method = __SERVICE, 'authenticate'
    args = [db, login, password, user_agent_env]
    
    return await rpc_result(http_client, url, service=service, method=method, args=args)


async def version(http_client: T_AsyncHttpClient, url: str = '') -> str:
    service, method = __SERVICE, 'version'
    
    return await rpc_result(http_client, url, service=service, method=method, ensure_instance_of=str)



@overload
async def about(http_client: T_AsyncHttpClient, url: str = '', *, extended: Literal[False]) -> str:
    ...


@overload
async def about(http_client: T_AsyncHttpClient, url: str = '', *, extended: Literal[True]) -> Tuple[str, str]:
    ...


async def about(http_client: T_AsyncHttpClient, url: str = '', *, extended):
    service, method = __SERVICE, 'about'
    args = [extended]
    
    return await rpc_result(http_client, url, service=service, method=method, args=args)

