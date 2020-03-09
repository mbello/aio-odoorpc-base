from typing import List, Optional, Union
from aio_odoorpc_base.protocols import T_HttpClient
from aio_odoorpc_base.sync.rpc import rpc_result


def execute_kw(http_client: T_HttpClient, url: str = '', *,
               db: str, uid: int, password: str,
               obj: str, method: str,
               args: list, kw: Optional[dict] = None) -> Union[bool, dict, int, List[dict], List[int]]:

    args = [db, uid, password, obj, method, [args]]

    if kw:
        args.append(kw)

    return rpc_result(http_client, url, service='object', method='execute_kw', args=args)
