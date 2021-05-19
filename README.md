## Base functions to pilot Odoo's jsonrpc API (aio-odoorpc-base)

### Description:
This python package implements a **complete** set of methods to access  
Odoo's external API (using jsonrpc rather than xmlrpc).

It offers an almost-exact mirror of Odoo's external API, even parameter names are the same.
It is 'almost-exact' because 'execute' is skipped in favor of 'execute_kw' only and the 
API methods from the 'db' service: 'list', 'drop', 'dump', 'rename', 'restore' are here 
implemented with names 'list_databases', 'drop_database', 'dump_database', 'rename_database'
and 'restore_database' respectively.  

The 'documentation' offered by this package is mostly in the form of proper type 
annotations so that you have a better idea of what kind of data each API method expects. 
Other than that, developers are recommended to go study Odoo's external API by reading the
source code at (https://github.com/odoo/odoo/tree/master/odoo/service). The three API services
'object', 'common' and 'db' are implemented there in files model.py, common.py and db.py 
respectively. On each of these python files, a 'dispatch' method is implemented for the service
in question. The methods available on the external service api are usually those prefixed with 
'exp_' in the method name, with the exception of the 'object' service which only exposes 
'execute' and 'execute_kw'.

All functions offered by this package are available in both async and sync versions.

### Available API RPC Methods:

#### 1. 'Common' API RPC Methods
check server-side implementation of these functions here:
https://github.com/odoo/odoo/blob/master/odoo/service/common.py

-----------------
- about(http_client, url, *, extended) -> Union[Tuple[str, str], str]
  ```python
  async def about(http_client: T_AsyncHttpClient, url: str = '', *, extended: bool) -> Union[Tuple[str, str], str]
  ```
  Tuple is returned only if extended is True
-----------------
- authenticate(http_client, url, *, db, login, password, user_agent_env)
  ```python
  async def authenticate(http_client: T_AsyncHttpClient, url: str = '', *, db: str, login: str, password: str, user_agent_env: Mapping) -> Union[int, Literal[False]]
  ```
  > The method `login` should be preferred over `authenticate`.
  
  Authenticate takes a `user_agent_env` dict.
  In the core implementation of the `res_users` model 
  (https://github.com/odoo/odoo/blob/master/odoo/addons/base/models/res_users.py#L709), 
  the `authenticate` method only looks for the key `base_location` and, if you are authenticating 
  with a system user and if the parameter 'web.base.url.freeze' in 'ir.config_parameter'
  if not True, this method will set 'web.base.url' to the value passed in
  `user_agent_env['base_location']`.
  If you do not understand all implications of changing 'web.base.url', and if you do not have a good reason
  to change 'web.base.url', you should not use this method and rely on 'login' instead.
  If user is not system user or if user_agent_env does not contain the 'base_location' key,
  a call to this method will only return the uid, just like 'login' does.

-----------------
- login(http_client, url, *, db, login, password)
  ```python
  async def login(http_client: T_AsyncHttpClient, url: str = '', *, db: str, login: str, password: str) -> Union[int, Literal[False]])
  ```
  The `login` call is really only a lookup of the user_id (an int) of a user given a
  database name, username and password. If you are using this RPC client over and over in your 
  code, maybe even calling from a stateless cloud service, you should consider finding out the 
  user id (uid) once and save it to avoid having to perform this one additional RPC call.
  
  The uid mentioned above is not a session-like id. It is really only the database id of the user and
  it never expires (the user could have its database id changed, which would be rare).
  There is really no `login` or `session initiation` step required to access 
  Odoo's external API if you know the uid and password from the beginning;
-----------------
- version(http_client, url)
  ```python
  async def version(http_client: T_AsyncHttpClient, url: str = '') -> str
  ```
  > Version is returned as a string (e.g. '14.0')
-----------------

#### 2. 'DB' API RPC Methods
check server-side implementation of these functions here:
https://github.com/odoo/odoo/blob/master/odoo/service/db.py


> ##### The following 'DB' RPC methods do not require user credentials to be called.
> ##### Consider them 'public' methods.
---
- db_exist(http_client, url, db_name)
  ```python
  async def db_exist(http_client: T_AsyncHttpClient, url: str = '', *, db_name: str) -> bool
  ```
---
- list_countries
  ```python
  async def list_countries(http_client: T_AsyncHttpClient, url: str = '') -> List[str]
  ```
---
- list_databases(http_client, url, *, document)
  ```python
  async def list_databases(http_client: T_AsyncHttpClient, url: str = '', *, document: bool = False) -> List[str]
  ```
---
- list_lang(http_client, url)
  ```python
  async def list_lang(http_client: T_AsyncHttpClient, url: str = '') -> List[str]
  ```
---
- server_version(http_client, url)
  ```python
  async def server_version(http_client: T_AsyncHttpClient, url: str = '') -> str
  ```
---

> #### The 'DB' methods below may have been disabled by the system admin.
> 
> #### The `list_db` configuration option controls whether they are enabled or disabled.
---
- change_admin_password(http_client, url, *_, admin_password, new_password)
  ```python
  async def change_admin_password(http_client: T_AsyncHttpClient, url: str = '', *args, admin_password: str, new_password: str) -> bool
  ```
---
- drop_database(http_client, url, *, admin_password, db_name)
  ```python
  async def drop_database(http_client: T_AsyncHttpClient, url: str = '', *, admin_password: str, db_name: str) -> bool
  ```
---
- dump_database(http_client, url, *, admin_password, db_name, format)
  ```python
  async def dump_database(http_client: T_AsyncHttpClient, url: str = '', *, admin_password: str, db_name: str, format: str = "zip") -> bytes:
  ```
  format can be 'zip' or any other value. If 'zip', the zipped file will also include the
  filestore, a manifest.json and the dump.sql.
  If format is any other value, you get raw dump.sql only
---
- migrate_databases
  ```python

  ```
---
- rename_database
  ```python

  ```
---
- restore_database
  ```python

  ```
---
- create_database(http_client, url, admin_password, db_name, demo, lang, user_password, login, country_code, phone)
  ```python
  async def create_database(http_client: T_AsyncHttpClient, url: str = '', *, admin_password: str, db_name: str, demo: bool, lang: str, user_password: str = 'admin', login: str = 'admin', country_code: str = None, phone: str = None) -> bool
  ```
---
- duplicate_database
  ```python

  ```
---


#### 3. 'Object' API RPC Methods
check server-side implementation of these functions here:
https://github.com/odoo/odoo/blob/master/odoo/service/model.py

- execute_kw(http_client, url, *, db, uid, password, obj, method, args, kwargs)
  ```python
  async def execute_kw(http_client: T_AsyncHttpClient, url: str = '', *, db: str, uid: int, password: str, obj: str, method: str, args: list, kwargs: Optional[dict] = None) -> Union[bool, dict, int, List[dict], List[int]]
  ```


All methods take as first 2 parameters:
- **http_client**: a callable or an instance of a compatible http_client (it must implement a 'post'
  method that accepts a 'url' and a 'json' parameter. Packages 'requests', 'httpx' and 'aiohttp' are 
  known to be compatible).
  If http_client is a callable, it will be called with a dict as the post payload and must return a 
  response object with a '.json()' method that may be synchronous or asynchronous (when using the async
  functions). It must return a dict-like object representing the reponse.

- **url**: the complete URL of your Odoo's jsonrpc endpoint. Usually something like
  'https://odoo.acme.com/jsonrpc' or 'https://odoo.acme.com:8443/jsonrpc'. 

Remaining parameters on each method are those expected by Odoo's external API, with identical names
as you will find on Odoo's source code. The method 'jsonrpc' is the low-level method in this package that
actually does all the HTTP calls for all implemented methods.

By default, when you issue 'from aio_odoorpc_base import ...' you will be importing the async methods.
If you want the sync methods you must import from 'aio_odoorpc_base.sync'. You may also use 
'aio_odoorpc_base.aio' if you prefer to be explicit on whether you are importing sync or async code.


### Also check aio-odoorpc: a higher-level API

In practice, you may notice that 99% of the time your calls to Odoo's RPC API go through the 'execute_kw'
or 'execute' method which is what allows you to deal with Odoo's models, reading and writing actual business
data  via the model methods 'search', 'read', 'search_read', 'search_count', 'write', 'create', etc.
While this package only offers you a bare 'execute_kw' method, the higher-level package 'aio-odoorpc' expands 
over this one adding easier to use objects and methods (such as 'search', 'read', 'search_read', 'search_count', 
'write', 'create', etc).

In other words, while this package is focused on mirring what is available on Odoo's external API in the simplest way, 
the package 'aio-odoorpc' is focused on offering a user-friendly interface to your Odoo instance, including dedicated
methods to access Odoo's model API which is probably what you will be using most.  

### No dependencies:
No dependency is not a promise, just a preference. It may change in the future, but only if for very
good reason.

While it would be easier if this package shipped with a specific http client dependency, it should be
noted that having the possibility to reuse HTTP sessions is a great opportunity to improve the 
speed of your running code. Also, it is possible that your project is already using some http client
library and here you have the opportunity to reuse it. 

Note that you must use an async http client library when using the async functions.

### Python HTTP Client packages known to be compatible:
- sync-only: 'requests'
- async-only: 'aiohttp'
- sync and async: 'httpx'

### Motivation:
The package 'odoorpc' is the most used and better maintained package to let you easily consume Odoo's
external API. It has lots of functionality, good documentation, a large user base and was developed
by people that are very experienced with Odoo in general and big contributors to the Odoo Community. 
In other words, if you are taking your first steps you should probably start with odoorpc.

However, for my needs, once I was developing Odoo integrations that needed to make hundreds of calls
to the Odoo API to complete a job, I began to sorely miss an async interface as well as more
control over the HTTP client used (I wished for HTTP2 support and connection polling/reuse).

Also, as I understood Odoo's external API, it started to sound like 'odoorpc' was too big for a task
too simple. For instance, most of the time (like 99% of the time), you will be calling to a single
jsonrpc method called 'execute_kw'. It is the same call over and over just changing the payload which 
itself is a simple json. THe package 'odoorpc' may be too heavy, a layer too thick if you do serious
Odoo RPC processing and need to optimize your code.

So I decided to develop a new package myself, made it async-first and tryed to keep it as simple as
possible. Also, I decided to split it in two, a very simple base package (this one) with only methods
that mirror those in Odoo's external API and another one 'aio-odoorpc' that adds another layer to
implement Odoo's model methods like 'search', 'search_read', 'read', etc. as well as an object model
to instantiate a class once and then make simple method invocation with few parameters to access 
what you need.


### Useful tips about Odoo's external API:

- The 'login' call is really only a lookup of the user_id (an int) of a user given a
  database name, user/login name and password. If you are using this RPC client over and over in your 
  code, maybe even calling from a stateless cloud service, you should consider finding out the 
  user id (uid) of the user and pass the uid instead of the username to the constructor of AsyncOdooRPC.
  This way, you do not need to call the login() RPC method to retrieve the uid, saving a RPC call;

- The uid mentioned above is not a session-like id. It is really only the database id of the user
  and it never expires. There is really no 'login' or 'session initiation' step required to access 
  Odoo's external API if you know the uid from the beginning;


### Other things to know about this module:
- It ships will a good suite of tests that run against an Odoo runbot instance;

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


### Usage

Ok, so let's start with some examples. I will omit the event_loop logic, I assume that if you want
to use an async module you already have that sorted out yourself or through a framework like FastAPI.

All examples below could also be called using the synchronous OdooRPC object, but without the
'await' syntax.

I recommend that you check the tests folder for many more examples. Also, the codebase is short,
do refer to it as well.

```
from aio_odoorpc_base.aio import login, execute_kw 
from aio_odoorpc_base.helpers import execute_kwargs
import httpx

url = 'https://odoo.acme.com/jsonrpc'

async with httpx.AsyncClient() as client:
    uid = await login(http_client=client, url=url, db='acme', login='demo', password='demo')
    kwargs = execute_kwargs(fields=['partner_id', 'date_order', 'amount_total'],
                            limit=1000, offset=0, order='amount_total DESC')
    data = await execute_kw(http_client=client,
                            url=url,
                            db='acme',
                            uid=uid,
                            password='demo',
                            obj='sale.order',
                            method='search_read',
                            args=[],
                            kw=kwargs)
```
