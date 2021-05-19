from typing import Literal, Mapping, Optional, Tuple, Union
from aio_odoorpc_base.protocols import T_AsyncHttpClient
from aio_odoorpc_base.aio.rpc import rpc_result

__SERVICE: str = 'common'


async def about(http_client: T_AsyncHttpClient, url: str = '', *_,
                extended: Optional[bool] = None) -> Union[str, Tuple[str, str]]:
    return await rpc_result(http_client, url, service=__SERVICE, method='about',
                            args=[] if extended is None else [True if extended else False],
                            ensure_instance_of=list if extended else str)


async def authenticate(http_client: T_AsyncHttpClient, url: str, db: str, login: str, password: str, *,
                       user_agent_env: Optional[Mapping] = None) -> Union[int, Literal[False]]:
    return await rpc_result(http_client, url, service=__SERVICE, method='authenticate',
                            args=[db, login, password, {} if user_agent_env is None else user_agent_env])


async def login(http_client: T_AsyncHttpClient, url: str, db: str, login: str,
                password: str) -> Union[int, Literal[False]]:
    return await rpc_result(http_client, url, service=__SERVICE, method='login',
                            args=[db, login, password])


async def set_loglevel(http_client: T_AsyncHttpClient, url: str = '', *_,
                       loglevel, logger: Optional[str] = None):
    args = [loglevel, logger] if logger is not None else [loglevel]
    return await rpc_result(http_client, url, service=__SERVICE, method='set_loglevel',
                            args=args, ensure_instance_of=bool)


async def version(http_client: T_AsyncHttpClient, url: str = '', *_) -> str:
    return await rpc_result(http_client, url, service=__SERVICE, method='version', ensure_instance_of=dict)
