from aio_odoorpc_base import login, execute_kw
from aio_odoorpc_base.helpers import odoo_base_url2jsonrpc_endpoint
from tests.test_fixtures import test_get_odoo_url_database
import httpx

url_db = test_get_odoo_url_database()

url = odoo_base_url2jsonrpc_endpoint(odoo_base_url=url_db[0][0])
db = url_db[0][1]

with httpx.Client(base_url=url) as client:
    uid = login(client, database=db, username='demo', password='demo')
    data = execute_kw(client,
                      database=db,
                      uid=uid,
                      password='demo',
                      model_name='sale.order',
                      method='search_read',
                      domain_or_ids=[],
                      kwargs={'fields': ['partner_id', 'date_order', 'amount_total'],
                              'limit': 20})

    print(data)

