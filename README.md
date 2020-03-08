## Base functions to pilot Odoo's jsonrpc API (aio-odoorpc-base)

---
#### Note:

A higher-level, friendlier interface is provided by aio-odoorpc, make sure to check that out
as well.

---

### Description:
This is a core/base package with lower-level functions used by other higher-level
'aio-odoorpc-*' packages that are used in production in at least one company.

All functions offered by this package are available in both async and sync versions. The sync
version is automatically generated from the async one, so they are always in sync! ;)

Here you will find methods to access Odoo's external API, mirroring the dispatching
methods available on Odoo's jsonrpc endpoint (i.e. 'login', 'execute_kw', etc).

If you know how Odoo's external API work, this package may very well suit all your needs. Otherwise,
if you prefer it a little higher level, you should check 'aio-odoorpc' which uses this package to
implement facilitating methods to call Odoo's model methods like 'search', search_read', 'read',
'search_count', 'write', 'create', etc. Ultimately, those methods are all implemented through 
'execute_kw' API calls which this package provides.
  

### No dependencies:
No dependency is not a promise, just a preference. It may change in the future, but only if for very
good reason.

This also means that you are free to use whatever HTTP Client library you like. This package only
requires that:
1. The http_client must support a '.post(url, json=a_dict)' method. All headers, etc must be
   managed by you. Alternatively, a callable can be passed on in place of the http client, in which
   case it will be called with a single argument: the json payload;
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

#####Python HTTP Client packages known to be compatible:
- sync-only: 'requests'
- async-only: 'aiohttp'
- sync and async: 'httpx'

### Motivation:
The package 'odoorpc' is the most used and better maintained package to let you easily consume Odoo's
jsonrpc API. It has lots of functionality, good documentation, a large user base and was developed
by people that are very experienced with Odoo in general and big contributors to the Odoo Community.  
In other words, if you are taking your first steps and do not need an async interface now, start with
odoorpc.

However, for my needs, once I was developing Odoo integrations that needed to make hundreds of calls
to the Odoo API to complete a single job, I began to sorely miss an async interface as well as more
control over the HTTP client used (I wished for HTTP2 support and connection reuse).

Also, as I understood Odoo's external API, it started to sound like 'odoorpc' was too big for a task
too simple. For instance, most of the time (like 99,99% of the time), you will be calling to a single
REST method called 'execute_kw'. It is the same call over and over just changing the payload which 
itself is a simple json. 

So I decided to develop a new package myself, made it async-first and tryed to keep it as simple as
possible. Also, I decided to split it in two, a very simple base package (this one) with only methods
that mirror those in Odoo's external API and another one 'aio-odoorpc' that adds another layer to
implement Odoo's model methods like 'search', 'search_read', 'read', etc. as well as an object model
to instantiate a class once and then make simple method invocation with few parameters to access 
what you need.  


### TO-DOs:
- Add functions to help getting data into Odoo, right now the functions are mostly to get data out;


### Other things to know about this module:
- It ships will a good suite of tests that run against an OCA runbot instance;

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
  

### Usage

Ok, so let's start with some examples. I will omit the event_loop logic, I assume that if you want
to use an async module you already have that sorted out yourself or through a framework like FastAPI.

All examples below could also be called using the synchronous OdooRPC object, but without the
'await' syntax. Synchronous functions do not start with 'aio_', that is a marker of the async
functions only.

I recommend that you check the tests folder for many more examples. Also, the codebase is very very short,
do refer to it as well.

```
from aio_odoorpc_base import aio_login, aio_execute_kw, build_odoo_jsonrpc_endpoint_url
import httpx

url = 'https://odoo.acme.com/jsonrpc'

async with httpx.AsyncHttpClient(url=url) as client:
    uid = await aio_login(http_client=client, database='acme', username='demo', password='demo')
    data = await aio_execute_kw(http_client=client,
                                database='acme',
                                uid=uid,
                                password='demo',
                                model_name='sale.order',
                                method='search_read',
                                method_arg=[],
                                method_kwargs = {'fields': ['partner_id', 'date_order', 'amount_total']}

```
