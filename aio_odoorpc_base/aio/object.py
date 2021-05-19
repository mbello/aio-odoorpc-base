from typing import List, Optional, Union
from aio_odoorpc_base.protocols import T_AsyncHttpClient
from aio_odoorpc_base.aio.rpc import rpc_result

__SERVICE: str = 'object'


async def execute_kw(http_client: T_AsyncHttpClient,
                     url: str,
                     db: str,
                     uid: int,
                     password: str,
                     *,
                     obj: str,
                     method: str,
                     args: list,
                     kwargs: Optional[dict] = None) -> Union[bool, dict, int, List[dict], List[int]]:
    
    url = '' if url is None else url
    return await rpc_result(http_client,
                            url,
                            service=__SERVICE,
                            method="execute_kw",
                            args=[db, uid, password, obj, method, args, kwargs])
