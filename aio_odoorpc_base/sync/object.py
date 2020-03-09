from typing import Any, Optional
from aio_odoorpc_base.protocols import T_HttpClient
from aio_odoorpc_base. import jsonrpc, check_jsonrpc_response


def execute_kw(http_client: T_HttpClient, url: str = '', *,
               database: str,
               uid: int,
               password: str,
               model_name: str,
               method: str,
               method_arg: list,
               method_kwargs: Optional[dict] = None) -> Any:

    args = [database, uid, password, model_name,
            method, [method_arg], method_kwargs]

    if method_kwargs is None:
        del args[-1]

    resp, req_id = jsonrpc(
        http_client, url, service='object', method='execute_kw', args=args)
    data = check_jsonrpc_response(resp, req_id)
    return data['result']
