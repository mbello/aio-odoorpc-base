from typing import Any, Mapping, Optional, Sequence, Tuple, Union
import random
from aio_odoorpc_base.protocols import T_HttpClient, T_Response


def jsonrpc(http_client: T_HttpClient,
            url: str = '', *,
            service: str,
            method: str,
            args: Optional[Sequence] = None,
            kwargs: Optional[Mapping] = None) -> Tuple[T_Response, int]:

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

    if callable(http_client):
        return http_client(json_payload)
    else:
        assert isinstance(json_payload, dict)
        print(json_payload)
        resp = http_client.post(url, json=json_payload)
        return resp, json_payload['id']


def check_jsonrpc_response(resp: T_Response,
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


def login(http_client: T_HttpClient,
          url: str = '', *,
          database: str,
          username: str,
          password: str) -> int:

    resp, req_id = jsonrpc(http_client, url,
                           service='common',
                           method='login',
                           args=[database, username, password])
    data = check_jsonrpc_response(resp, req_id, ensure_instance_of=int)
    return data['result']


def execute_kw(http_client: T_HttpClient,
               url: str = '', *,
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

    resp, req_id = jsonrpc(http_client, url,
                           service='object',
                           method='execute_kw',
                           args=args)
    data = check_jsonrpc_response(resp, req_id)
    return data['result']
