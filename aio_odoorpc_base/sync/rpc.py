import random
from typing import List, Mapping, Optional, Sequence, Tuple, Union
from aio_odoorpc_base.protocols import T_HttpClient, T_Response

EARLY_CONTEXT: Optional[dict] = None


def get_early_context(tree, *args) -> Optional[dict]:
    if tree is None:
        return None

    last_leaf = (len(args) == 1)

    next_d = tree.get(args[0])
    if next_d is None and not last_leaf and 'default' not in tree:
        next_d = tree.get('*')
    else:
        return tree.get('default')

    return next_d if last_leaf else get_early_context(next_d, *args[1:])


def jsonrpc(http_client: T_HttpClient, url: str = '', *,
            service: str, method: str,
            args: Optional[Sequence] = None,
            kwargs: Optional[Mapping] = None) -> Tuple[T_Response, int]:

    json_payload = {'jsonrpc': '2.0',
                    'method': 'call',
                    'context': get_early_context(EARLY_CONTEXT, url, service, method),
                    'params': {'service': service,
                               'method': method,
                               'args': [] if args is None else args,
                               'kwargs': kwargs},
                    'id': random.randint(0, 1000000000)}

    if json_payload['context'] is None:
        del json_payload['context']
    if kwargs is None:
        del json_payload['params']['kwargs']

    if callable(http_client):
        resp = http_client(url, json_payload)
    else:
        resp = http_client.post(url, json=json_payload)

    return resp, json_payload['id']


def check_jsonrpc_response(resp: T_Response,
                           req_id: int,
                           ensure_instance_of: Optional[type] = None) -> Mapping:
    data = resp.json()

    if data.get('id') != req_id:
        raise RuntimeError(
            "[aio-odoorpc-base] Somehow the response id differs from the request id.")

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


def rpc_call_and_check(http_client: T_HttpClient, url: str = '', *,
                       service: str, method: str,
                       args: Optional[Sequence] = None,
                       kwargs: Optional[Mapping] = None,
                       ensure_instance_of: Optional[type] = None) -> Mapping:
    resp, req_id = jsonrpc(http_client, url, service=service,
                           method=method, args=args, kwargs=kwargs)
    return check_jsonrpc_response(resp, req_id, ensure_instance_of=ensure_instance_of)


def rpc_result(http_client: T_HttpClient, url: str = '', *,
               service: str, method: str,
               args: Optional[Sequence] = None,
               kwargs: Optional[Mapping] = None,
               ensure_instance_of: Optional[type] = None) -> Union[bool, bytes, dict, int, str,
                                                                   List[dict], List[int], List[str]]:
    data = rpc_call_and_check(http_client=http_client, url=url, service=service, method=method,
                              args=args, kwargs=kwargs, ensure_instance_of=ensure_instance_of)
    return data['result']
