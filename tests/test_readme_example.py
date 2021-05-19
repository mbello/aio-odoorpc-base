import pytest
import httpx
from aio_odoorpc_base.aio import execute_kw
from aio_odoorpc_base.helpers import execute_kwargs


@pytest.mark.asyncio
@pytest.mark.auto
async def test_readme_example(base_args_obj):
    async with httpx.AsyncClient() as client_:
        client, url, db, uid, pwd = base_args_obj(client_)
        kwargs = execute_kwargs(fields=['partner_id', 'date_order', 'amount_total'],
                                limit=5, offset=0, order='amount_total DESC')
        data = await execute_kw(http_client=client,
                                url=url,
                                db=db,
                                uid=uid,
                                password=pwd,
                                obj='sale.order',
                                method='search_read',
                                args=[],
                                kwargs=kwargs)
        assert len(data) == 5
        assert len(data[0].keys()) == 4
