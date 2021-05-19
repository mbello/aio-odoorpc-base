from typing import List, Optional, Union
from aio_odoorpc_base.protocols import T_HttpClient
from aio_odoorpc_base.sync.rpc import rpc_result

__SERVICE: str = 'object'


def execute_kw(http_client: T_HttpClient,
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
    return rpc_result(http_client,
                      url,
                      service=__SERVICE,
                      method="execute_kw",
                      args=[db, uid, password, obj, method, args, kwargs])
