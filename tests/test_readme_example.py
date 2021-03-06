import pytest
import httpx
from aio_odoorpc_base.aio import login, execute_kw
from aio_odoorpc_base.helpers import execute_kwargs


@pytest.mark.asyncio
async def test_readme_example(url_db_user_pwd: list):
    url, db, user, pwd = url_db_user_pwd
    
    async with httpx.AsyncClient() as client:
        uid = await login(http_client=client, url=url, db=db, login=user, password=pwd)
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
                                kw=kwargs)
        assert len(data) == 5
        assert len(data[0].keys()) == 4
