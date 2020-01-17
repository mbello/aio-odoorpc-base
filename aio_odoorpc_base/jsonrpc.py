from typing import Any, Mapping, Optional, Sequence, Tuple
import random
from aio_odoorpc_base.protocols import ProtoHttpClient, ProtoResponse
# from asyncio import iscoroutine


def jsonrpc(http_client: ProtoHttpClient, *,
            service: str,
            method: str,
            args: Optional[Sequence] = None,
            kwargs: Optional[Mapping] = None) -> Tuple[ProtoResponse, int]:

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

    return http_client.post('', json=json_payload), json_payload['id']


def check_jsonrpc_response(resp: ProtoResponse,
                           req_id: int,
                           ensure_instance_of: Optional[type] = None) -> Mapping:

    data = resp.json()
    assert data.get(
        'id') == req_id, "[aio-odoorpc-base] Somehow the response id differs from the request id."

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


def login(http_client: ProtoHttpClient, *,
          database: str,
          username: str,
          password: str) -> int:
    resp, req_id = jsonrpc(http_client=http_client,
                           service='common',
                           method='login',
                           args=[database, username, password])
    return (check_jsonrpc_response(resp, req_id, ensure_instance_of=int))['result']


def execute_kw(http_client: ProtoHttpClient, *,
               database: str,
               uid: int,
               password: str,
               model_name: str,
               method: str,
               domain_or_ids: list,
               kwargs: Optional[dict] = None) -> Any:

    args = [database, uid, password, model_name,
            method, [domain_or_ids], kwargs]

    if kwargs is None:
        del args[-1]

    resp, req_id = jsonrpc(http_client=http_client,
                           service='object',
                           method='execute_kw',
                           args=args)
    return (check_jsonrpc_response(resp, req_id))['result']
