## Base functions to pilot Odoo's jsonrpc API (aio-odoorpc-base)

---
#### Note:

A higher-level, friendler interface is provided by aio-odoorpc, make sure to check that out
as well.

This is a fast, simple Odoo RPC client that offers two versions of the same API:
1. AsyncOdooRPC: asynchronous version;
2. OdooRPC: the 'normal', synchronous version.

---

### Description:
This is a core/base package with lower-level functions used by other higher-level
'aio-odoorpc-*' packages that are used in production in at least one company.

All functions offered by this package are available in both async and sync versions. The sync
version is automatically generated from the async one, so they are always in sync! ;)

While lacking some sort of facilitating helper class, the functions provided by this package
are quite usable and may be a very good foundation for your own Odoo-interfacing code.

Do not at all expect to find functionality similar to erpeek or odoorpc, this package only offers
facilitating functions that mirror the dispatching methods available on Odoo's jsonrpc endpoint
(i.e. 'login', 'execute_kw', etc).

You will not find facilitating functions for methods such as 'search', 'read', 'search_read' which
are actually executed through the 'execute_kw' dispatcher. If you want those higher-level functions
you should probably look into 'aio-odoorpc'.


### No dependencies:
No dependency is not a promise, just a preference. It may change in the future, but only if for very
good reason.

This also means that you are free to use whatever HTTP Client library you like. This package only
requires that:
1. The http_client must support a '.post(json=a_dict)' method that should be happy with a single
   'json' named argument. All headers, etc must be managed by you;
2. The 'post' method mentioned above must return a response object that must have a '.json()'
   method. This method may be synchronous or asynchronous (when using the async functions).
   It must return a dict or dict-like object. This interface is supported by packages such
   as 'requests', 'httpx' and 'aiohttp'. If your favorite library does not offer such interface, it
   is easy to wrap the object yourself in order to provide it;

I am willing to make modifications in the code in order to support other http client solutions, just
get in touch (use the project's github repository for that).

While it would be easier if this package shipped with a specific http client dependency, it should be
noted that having the possibility to reuse HTTP sessions is a great opportunity to improve the 
speed of your running code. Also, it is possible that your project is already using some http client
library and here you have the opportunity to use it. 

Remember that you must use an async http client library if you are going to use the async functions,
or use a synchronous http client library if you are going to use the sync function.

- sync-only http client options: 'requests'
- async-only http client options: 'aiohttp'
- sync and async http client options: 'httpx'

### Motivation:
As I gained experience producing code to interface with Odoo's RPC API, I felt that it was better to control myself
all the RPC invocations and hence I started to use only the lower level 'odoorpc' methods
(execute_kw, read, search, search_read).
The package 'odoorpc' is a great solution to pilot Odoo, it offers plenty of functionality, but it does
get in the way when one needs to go fast, specially when you are making thousands of remote RPC calls.
Also, if you want fast code you quickly start missing an async interface. So here it is, enjoy!


### TO-DOs:
- Add functions to help getting data into Odoo, right now the functions are mostly to get data out;
- Add tests. However, I do run tests from higher-level code that depend on this package so I have
  indirect ways to test this codebase. Not ideal, but enough for now.


### Other things to know about this module:
- Asyncio is a python3 thing, so no python2 support;

- Type hints are used everywhere;

- This package uses jsonrpc only (no xmlrpc). There is a lack of async xmlrpc tooling and
  jsonrpc is considered the best RPC protocol in Odoo (faster, more widely used);
  
- The synchronous version of the code is generated automatically from the asynchronous code, so at
  least for now the effort to maintain both is minimal.

- I am willing to take patches and to add other contributors to this project. Feel free to get in touch,
  the github page is the best place to interact with the project and the project's author;

- I only develop and run code in Linux environments, if you find a bug under other OS I am happy
  to take patches but I will not myself spend time looking into these eventual bugs;


### Things to know about Odoo RPC API:

- The 'login' call is really only a lookup of the user_id (an int) of a user given a
  database, username and password. If you are using this RPC client over and over in your code,
  maybe even calling from a stateless cloud service, you should consider finding out the user id (uid)
  of the user and pass the uid instead of the username to the constructor of AsyncOdooRPC. This way, 
  you do not need to call the login() RPC method to retrieve the uid, saving a RPC call;

- The uid mentioned above is not a session-like id. It is really only the database id of the user
  and it never expires. There is really no 'login' step required to access the Odoo RPC API if you
  know the uid from the beginning;
  
- Odoo can be quite slow (although v13 improves things a lot!). Sorry, nothing we can do here, 
  whatever optimization may exist in this package may reduce the execution time by a fraction of
  a millisecond. This is nothing compared with the latency of network data transmission and RPC calls.
  If you do find opportunities for optimization, let me know. Just don't blame this package first, it
  is unlikely to be the culprit if your code is running slowly.


### Usage

Ok, so let's start with some examples. I will omit the event_loop logic, I assume that if you want
to use an async module you already have that sorted out yourself or through a framework like FastAPI.

All examples below could also be called using the synchronous OdooRPC object, but without the
'await' syntax. Synchronous functions do not start with 'aio_', that is a marker of the async
functions only.

```
from aio_odoorpc_base import aio_login, aio_execute_kw, build_odoo_jsonrpc_endpoint_url
import httpx

url = build_odoo_jsonrpc_endpoint_url(host='acme.odoo.com')

async with httpx.AsyncHttpClient(url=url) as client:
    uid = await aio_login(client, database='acme', username='demo', password='demo')
    data = await aio_execute_kw(client,
                                database='acme',
                                uid=uid,
                                password='demo',
                                model_name='sale.order',
                                method='search_read',
                                domain_or_ids=[[]],
                                kwargs = {'fields': ['} 


# if server is listening on default http/https ports, there is no need to specify the port
# in the url. Otherwise, url could be "https://acme.odoo.com:8069" to specify the port number.
# Remember, the method __init__ is never a coroutine, so no await here. But we make no blocking
# calls on the __init__ method.

client = AsyncOdooRPC(url = "https://acme.odoo.com",
                      database = "acme",
                      username_or_uid = "joe@acme.com",
                      password = "my super-difficult-to-guess password")

# login is only required because the client was instantiated with a username rather than a
# user id (uid).
await client.login()

# or we can instantiate the class using a helper. With the helper, there is no need to 
# call the login() method, it takes care of it for you if necessary.
client = await AsyncOdooRPC.from_cfg(host = "acme.odoo.com",
                                     database = "acme",
                                     username = "joe@acme.com",
                                     password = "my super-difficult-to-guess password",
                                     port = 8069,
                                     ssl = True,
                                     ssl_verify = True)
```

## Ok, so now that you have a class instance, let's use it! 

```
    data = await client.search_read(model_name='sale.order',
                                    domain=[['date_confirmed', '>=', '2019-01-01]],
                                    fields=['number, date_confirmed, order_total'],
                                    limit=500)
```
