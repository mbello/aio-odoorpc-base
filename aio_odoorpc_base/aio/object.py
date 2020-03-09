from typing import List, Optional, Union
from aio_odoorpc_base.protocols import T_AsyncHttpClient
from aio_odoorpc_base.aio.rpc import rpc_result


async def execute_kw(http_client: T_AsyncHttpClient, url: str = '', *,
                     db: str, uid: int, password: str,
                     obj: str, method: str,
                     args: list, kw: Optional[dict] = None) -> Union[bool, dict, int, List[dict], List[int]]:

    args = [db, uid, password, obj, method, [args]]
    
    if kw:
        args.append(kw)
    
    return await rpc_result(http_client, url, service='object', method='execute_kw', args=args)
