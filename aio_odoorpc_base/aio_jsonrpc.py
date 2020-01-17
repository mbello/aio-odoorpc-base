from typing import Any, Mapping, Optional, Sequence, Tuple
import random
from aio_odoorpc_base.protocols import ProtoAsyncHttpClient, ProtoAsyncResponse, ProtoResponse
from asyncio import iscoroutine


async def aio_jsonrpc(http_client: ProtoAsyncHttpClient, *,
                      service: str,
                      method: str,
                      args: Optional[Sequence] = None,
                      kwargs: Optional[Mapping] = None) -> Tuple[ProtoResponse or ProtoAsyncResponse, int]:
    
    json_payload = {'jsonrpc': '2.0',
                    'method': 'call',
                    'params': {'service': service,
                               'method': method,
                               'args': args,
                               'kwargs': kwargs},
                    'id': random.randint(0, 1000000000)}
    
    if args is None:
        del json_payload['params']['args']
    if kwargs is None:
        del json_payload['params']['kwargs']
        
    return await http_client.post('', json=json_payload), json_payload['id']


async def aio_check_jsonrpc_response(resp: ProtoResponse or ProtoAsyncResponse,
                                     req_id: int,
                                     ensure_instance_of: Optional[type] = None) -> Mapping:
    
    data = await resp.json() if iscoroutine(resp.json) else resp.json()
    assert data.get('id') == req_id, "[aio-odoorpc-base] Somehow the response id differs from the request id."
    
    if data.get('error'):
        raise RuntimeError(data['error'])
    else:
        result = data.get('result')
        if result is None:
            raise RuntimeError('[aio-odoorpc-base] Response with no result.')
        if ensure_instance_of is not None:
            assert isinstance(result, ensure_instance_of), \
                f'[aio-odoorpc-base] Result of unexpected type. ' \
                f'Expecting {type(ensure_instance_of)}, got {type(result)}.'
        return data


async def aio_login(http_client: ProtoAsyncHttpClient, *,
                    database: str,
                    username: str,
                    password: str) -> int:
    resp, req_id = await aio_jsonrpc(http_client=http_client,
                                     service='common',
                                     method='login',
                                     args=[database, username, password])
    return (await aio_check_jsonrpc_response(resp, req_id, ensure_instance_of=int))['result']


async def aio_execute_kw(http_client: ProtoAsyncHttpClient, *,
                         database: str,
                         uid: int,
                         password: str,
                         model_name: str,
                         method: str,
                         domain_or_ids: list,
                         kwargs: Optional[dict] = None) -> Any:
    
    args = [database, uid, password, model_name, method, [domain_or_ids], kwargs]
    
    if kwargs is None:
        del args[-1]
    
    resp, req_id = await aio_jsonrpc(http_client=http_client,
                                     service='object',
                                     method='execute_kw',
                                     args=args)
    return (await aio_check_jsonrpc_response(resp, req_id))['result']
