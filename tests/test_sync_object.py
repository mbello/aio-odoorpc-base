import pytest
from aio_odoorpc_base.sync.object import execute_kw
import asyncio
import httpx


@pytest.mark.auto
def test_sync_login_search_read(base_args_obj):
    with httpx.Client() as client_:
        client, url, db, uid, pwd = base_args_obj(client_)
        model_name = 'sale.order'
        fields = ['partner_id', 'date_order', 'amount_total']
        exkw_kwargs = {'http_client': client,
                       'url': url,
                       'db': db,
                       'uid': uid,
                       'password': pwd,
                       'obj': model_name,
                       'method': 'search_read',
                       'args': [],
                       'kwargs': {'fields': fields}}

        data1 = execute_kw(**exkw_kwargs)

        exkw_kwargs['method'] = 'search_count'
        exkw_kwargs['args'] = [[]]  # needs a domain, even if empty
        exkw_kwargs['kwargs'] = None
        count = execute_kw(**exkw_kwargs)

        exkw_kwargs['method'] = 'search'
        ids = execute_kw(**exkw_kwargs)

        exkw_kwargs['method'] = 'read'
        exkw_kwargs['args'] = [ids]
        exkw_kwargs['kwargs'] = {'fields': fields}
        data2 = execute_kw(**exkw_kwargs)

        count = count
        data1 = data1
        data2 = data2

        assert len(data1) == count
        assert len(ids) == count
        assert len(data2) == count

        if 'id' not in fields:
            fields.append('id')

        for f in fields:
            for d in data1:
                assert f in d

        for f in fields:
            for d in data2:
                assert f in d

        ids1 = [d.get('id') for d in data1]
        ids2 = [d.get('id') for d in data2]
        ids.sort()
        ids1.sort()
        ids2.sort()

        assert len(ids) == len(ids1) and len(ids) == len(ids2)

        data1 = {d.get('id'): d for d in data1}
        data2 = {d.get('id'): d for d in data2}

        for i in range(0, len(ids) - 1):
            assert ids[i] == ids1[i] == ids2[i]

        for f in fields:
            assert data1[ids[i]][f] == data2[ids[i]][f]
