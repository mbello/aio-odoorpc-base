import pytest
from aio_odoorpc_base import login, execute_kw, build_odoo_jsonrpc_endpoint_url, odoo_base_url2jsonrpc_endpoint
from aio_odoorpc_base.protocols import T_HttpClient
import httpx
import requests


def test_sync_httpx1(url_db_user_pwd: list, aio_benchmark):
    url, db, user, pwd = url_db_user_pwd
    with httpx.Client(base_url=url) as session:
        aio_benchmark(sync_login_search_read, '', db, user, pwd, session)


@pytest.mark.benchmark
def test_sync_httpx2(url_db_user_pwd: list, aio_benchmark):
    url, db, user, pwd = url_db_user_pwd
    with httpx.Client() as session:
        aio_benchmark(sync_login_search_read, url, db, user, pwd, session)


@pytest.mark.benchmark
def test_sync_requests(url_db_user_pwd: list, aio_benchmark):
    url, db, user, pwd = url_db_user_pwd
    with requests.Session() as session:
        aio_benchmark(sync_login_search_read, url, db, user, pwd, session)

def test_urls():
    url = build_odoo_jsonrpc_endpoint_url(host='odoo.com', port=80,
                                          ssl=True)
    assert url == 'https://odoo.com:80/jsonrpc'
    url = build_odoo_jsonrpc_endpoint_url(host='odoo.com', port=80,
                                          ssl=False)
    assert url == 'http://odoo.com/jsonrpc'
    url = build_odoo_jsonrpc_endpoint_url(host='odoo.com', port=443,
                                          ssl=True, base_url='acme')
    assert url == 'https://odoo.com/acme/jsonrpc'
    url = build_odoo_jsonrpc_endpoint_url(host='odoo.com', port=8069,
                                          ssl=True, base_url='acme', custom_odoo_jsonrpc_suffix='jrpc')
    assert url == 'https://odoo.com:8069/acme/jrpc'
    
    url = build_odoo_jsonrpc_endpoint_url(host='odoo.com',
                                          ssl=True, base_url='acme', custom_odoo_jsonrpc_suffix='jrpc')
    assert url == 'https://odoo.com/acme/jrpc'
    url = build_odoo_jsonrpc_endpoint_url(host='odoo.com',
                                          ssl=False, base_url='acme')
    assert url == 'http://odoo.com/acme/jsonrpc'
    
    url = odoo_base_url2jsonrpc_endpoint(odoo_base_url='http://odoo.com/')
    assert url == 'http://odoo.com/jsonrpc'

    url = odoo_base_url2jsonrpc_endpoint(odoo_base_url='http://odoo.com')
    assert url == 'http://odoo.com/jsonrpc'

    url = odoo_base_url2jsonrpc_endpoint()
    assert url == 'jsonrpc'
    
    url = odoo_base_url2jsonrpc_endpoint(custom_odoo_jsonrpc_suffix='superrpc')
    assert url == 'superrpc'
    
    url = odoo_base_url2jsonrpc_endpoint(custom_odoo_jsonrpc_suffix='/superrpc')
    assert url == 'superrpc'

    url = odoo_base_url2jsonrpc_endpoint(odoo_base_url='http://odoo.com', custom_odoo_jsonrpc_suffix='/jsonrpc')
    assert url == 'http://odoo.com/jsonrpc'

    url = odoo_base_url2jsonrpc_endpoint(odoo_base_url='http://odoo.com/', custom_odoo_jsonrpc_suffix='/jsonrpc')
    assert url == 'http://odoo.com/jsonrpc'

    url = odoo_base_url2jsonrpc_endpoint(odoo_base_url='http://odoo.com////', custom_odoo_jsonrpc_suffix='///jsonrpc')
    assert url == 'http://odoo.com/jsonrpc'


def sync_login_search_read(url: str, db: str, user: str, pwd: str, session: T_HttpClient):
    
    uid = login(session, url, database=db, username=user, password=pwd)
    limit = 10
    fields = ['partner_id', 'date_order', 'amount_total']
    exkw_kwargs = {'http_client': session,
                   'url': url,
                   'database': db,
                   'uid': uid,
                   'password': pwd,
                   'model_name': 'sale.order',
                   'method': 'search_read',
                   'domain_or_ids': [],
                   'kwargs': {'fields': fields}}
    
    data1 = execute_kw(**exkw_kwargs)
    
    exkw_kwargs['method'] = 'search_count'
    exkw_kwargs['kwargs'] = None
    count = execute_kw(**exkw_kwargs)
    
    exkw_kwargs['method'] = 'search'
    ids = execute_kw(**exkw_kwargs)
    
    exkw_kwargs['method'] = 'read'
    exkw_kwargs['domain_or_ids'] = ids
    exkw_kwargs['kwargs'] = {'fields': fields}
    data2 = execute_kw(**exkw_kwargs)
    
    assert len(data1) == count
    assert len(ids) == count
    assert len(data2) == count
    
    if 'id' not in fields:
        fields.append('id')
    
    for f in fields:
        for d in data1:
            assert d.get(f)

    for f in fields:
        for d in data2:
            assert d.get(f)

    ids1 = [d.get('id') for d in data1]
    ids2 = [d.get('id') for d in data2]
    ids.sort()
    ids1.sort()
    ids2.sort()
    
    assert len(ids) == len(ids1) and len(ids) == len(ids2)

    data1 = {d.get('id'): d for d in data1}
    data2 = {d.get('id'): d for d in data2}
    
    for i in range(0, len(ids)-1):
        assert ids[i] == ids1[i] == ids2[i]
        
        for f in fields:
            assert data1[ids[i]][f] == data2[ids[i]][f]
    