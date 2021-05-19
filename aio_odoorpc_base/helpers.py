from typing import Dict, List, Mapping, Optional, Union


def execute_kwargs(*,
                   fields: Optional[List[str]] = None,
                   limit: Optional[int] = None,
                   offset: Optional[int] = None,
                   order: Optional[str] = None,
                   count: Optional[bool] = None,
                   context: Optional[Mapping[str, Union[str, int]]] = None) \
        -> Optional[Dict[str, Union[str, int, bool, List[str], Dict[str, Union[str, int]]]]]:
    kwargs = dict()
    if offset is not None:
        kwargs['offset'] = offset
    if limit is not None:
        kwargs['limit'] = limit
    if order is not None:
        kwargs['order'] = order
    if fields is not None:
        kwargs['fields'] = fields
    if count is not None:
        kwargs['count'] = count
    if context is not None:
        kwargs['context'] = context
    return kwargs if kwargs else None


def build_odoo_jsonrpc_endpoint_url(*,
                                    host: str,
                                    port: Optional[int] = None,
                                    ssl: bool = True,
                                    base_url: str = '',
                                    jsonrpc_suffix: str = 'jsonrpc') -> str:
    jsonrpc_suffix = jsonrpc_suffix.strip('/')
    url = build_odoo_base_url(host=host, port=port, ssl=ssl, base_url=base_url)
    return f'{url}/{jsonrpc_suffix}'


def build_odoo_base_url(*,
                        host: str,
                        port: Optional[int] = None,
                        ssl: bool = True,
                        base_url: str = '') -> str:
    url_protocol = 'https' if ssl else 'http'
    host = host.strip('/')
    if port is None:
        port = 443 if ssl else 80
    else:
        port = int(port)
    port = '' if (port == 80 and not ssl) or (port == 443 and ssl) else f':{port}'
    base_url = base_url.strip('/')
    base_url = '/' + base_url if len(base_url) > 0 else ''
    return f'{url_protocol}://{host}{port}{base_url}'


def odoo_base_url2jsonrpc_endpoint(odoo_base_url: str = '',
                                   jsonrpc_suffix: str = 'jsonrpc') -> str:
    suffix = jsonrpc_suffix.strip('/')
    suffix = '/' + suffix if len(suffix) > 0 else ''
    if not odoo_base_url:
        return suffix
    odoo_base_url = odoo_base_url.strip('/')
    return f'{odoo_base_url}{suffix}' if not odoo_base_url.endswith(suffix) else odoo_base_url


def jsonrpc_endpoint2odoo_base_url(jsonrpc_url: str = '',
                                   jsonrpc_suffix: str = 'jsonrpc') -> str:
    jsonrpc_url = jsonrpc_url.strip('/')
    suffix = jsonrpc_suffix.strip('/')
    suffix = '/' + suffix if len(suffix) > 0 else ''
    return jsonrpc_url if not jsonrpc_url.endswith(suffix) else jsonrpc_url[:-len(suffix)].strip('/')
