import pytest
from aio_odoorpc_base.helpers import build_odoo_jsonrpc_endpoint_url, odoo_base_url2jsonrpc_endpoint, \
    build_odoo_base_url, execute_kwargs, jsonrpc_endpoint2odoo_base_url


@pytest.mark.auto
def test_helpers_build_odoo_jsonrpc_endpoint_url():
    url = build_odoo_jsonrpc_endpoint_url(host='odoo.com', port=80, ssl=True)
    assert url == 'https://odoo.com:80/jsonrpc'
    url = build_odoo_jsonrpc_endpoint_url(host='odoo.com', port=80, ssl=False)
    assert url == 'http://odoo.com/jsonrpc'
    url = build_odoo_jsonrpc_endpoint_url(host='odoo.com', port=443, ssl=True, base_url='acme')
    assert url == 'https://odoo.com/acme/jsonrpc'
    url = build_odoo_jsonrpc_endpoint_url(host='odoo.com', port=8069, ssl=True, base_url='acme',
                                          jsonrpc_suffix='jrpc')
    assert url == 'https://odoo.com:8069/acme/jrpc'
    url = build_odoo_jsonrpc_endpoint_url(host='odoo.com', ssl=True, base_url='acme',
                                          jsonrpc_suffix='jrpc')
    assert url == 'https://odoo.com/acme/jrpc'
    url = build_odoo_jsonrpc_endpoint_url(host='odoo.com', ssl=False, base_url='acme')
    assert url == 'http://odoo.com/acme/jsonrpc'
    

@pytest.mark.auto
def test_helpers_odoo_base_url2jsonrpc_endpoint():
    url = odoo_base_url2jsonrpc_endpoint(odoo_base_url='http://odoo.com/')
    assert url == 'http://odoo.com/jsonrpc'
    url = odoo_base_url2jsonrpc_endpoint(odoo_base_url='http://odoo.com')
    assert url == 'http://odoo.com/jsonrpc'
    url = odoo_base_url2jsonrpc_endpoint()
    assert url == '/jsonrpc'
    url = odoo_base_url2jsonrpc_endpoint(jsonrpc_suffix='superrpc')
    assert url == '/superrpc'
    url = odoo_base_url2jsonrpc_endpoint(jsonrpc_suffix='/superrpc')
    assert url == '/superrpc'
    url = odoo_base_url2jsonrpc_endpoint(odoo_base_url='http://odoo.com', jsonrpc_suffix='/rpc')
    assert url == 'http://odoo.com/rpc'
    url = odoo_base_url2jsonrpc_endpoint(odoo_base_url='https://odoo.com:8080/', jsonrpc_suffix='jrpc')
    assert url == 'https://odoo.com:8080/jrpc'
    url = odoo_base_url2jsonrpc_endpoint(odoo_base_url='https://odoo.com:8080', jsonrpc_suffix='jrpc')
    assert url == 'https://odoo.com:8080/jrpc'
    url = odoo_base_url2jsonrpc_endpoint(odoo_base_url='http://odoo.com////', jsonrpc_suffix='///jsonrpc')
    assert url == 'http://odoo.com/jsonrpc'
    url = odoo_base_url2jsonrpc_endpoint(odoo_base_url='//http://odoo.com/superrpc//', jsonrpc_suffix='superrpc')
    assert url == 'http://odoo.com/superrpc'
    url = odoo_base_url2jsonrpc_endpoint(odoo_base_url='http://odoo.com/jsonrpc/')
    assert url == 'http://odoo.com/jsonrpc'


@pytest.mark.auto
def test_helpers_build_odoo_base_url():
    url = build_odoo_base_url(host='odoo.com', port=80, ssl=True)
    assert url == 'https://odoo.com:80'
    url = build_odoo_base_url(host='odoo.com', port=80, ssl=False)
    assert url == 'http://odoo.com'
    url = build_odoo_base_url(host='odoo.com', port=443, ssl=True, base_url='acme/yes')
    assert url == 'https://odoo.com/acme/yes'
    url = build_odoo_base_url(host='odoo.com', port=8069, ssl=True, base_url='acme')
    assert url == 'https://odoo.com:8069/acme'
    url = build_odoo_base_url(host='odoo.com', ssl=True, base_url='acme')
    assert url == 'https://odoo.com/acme'
    url = build_odoo_base_url(host='odoo.com', ssl=False, base_url='//acme//')
    assert url == 'http://odoo.com/acme'


@pytest.mark.auto
def test_helpers_jsonrpc_endpoint2odoo_base_url():
    url = jsonrpc_endpoint2odoo_base_url(jsonrpc_url='https://www.odoo.com/acme/jsonrpc')
    assert url == 'https://www.odoo.com/acme'
    url = jsonrpc_endpoint2odoo_base_url(jsonrpc_url='/https://www.odoo.com/acme//jsonrpc///')
    assert url == 'https://www.odoo.com/acme'
    url = jsonrpc_endpoint2odoo_base_url(jsonrpc_url='/https://www.odoo.com/acme/jsonrpc',
                                         jsonrpc_suffix='customrpc')
    assert url == 'https://www.odoo.com/acme/jsonrpc'
    url = jsonrpc_endpoint2odoo_base_url(jsonrpc_url='/https://www.odoo.com/acme/customrpc',
                                         jsonrpc_suffix='customrpc')
    assert url == 'https://www.odoo.com/acme'
    url = jsonrpc_endpoint2odoo_base_url(jsonrpc_url='https://www.odoo.com/acme/myviewjsonrpc')
    assert url == 'https://www.odoo.com/acme/myviewjsonrpc'


@pytest.mark.auto
def test_helpers_execute_kwargs():
    d = execute_kwargs(fields=None, limit=None, offset=None, order=None, count=None, context=None)
    assert d is None
    d = execute_kwargs(fields=['a'])
    assert 'fields' in d and len(d) == 1
    d = execute_kwargs(limit=100)
    assert 'limit' in d and len(d) == 1
    d = execute_kwargs(offset=10)
    assert 'offset' in d and len(d) == 1
    d = execute_kwargs(order='a')
    assert 'order' in d and len(d) == 1
    d = execute_kwargs(count=True)
    assert 'count' in d and len(d) == 1
    d = execute_kwargs(context={'ctx': 10})
    assert 'context' in d and len(d) == 1
    d = execute_kwargs(fields=['a'], limit=30, offset=1000, count=False)
    assert 'fields' in d and 'limit' in d and 'offset' in d and 'count' in d and len(d) == 4
