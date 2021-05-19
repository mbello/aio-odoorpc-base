import pytest
import httpx
import zipfile
import io
import string
import secrets
import time
from typing import Any, Optional, Tuple
from aio_odoorpc_base.aio.db import db_exist, list_countries, list_databases, \
    list_lang, server_version, change_admin_password, create_database, drop_database, \
    dump_database, duplicate_database, migrate_databases, rename_database, restore_database


@pytest.mark.asyncio
@pytest.mark.auto
async def test_async_db_db_exist(base_args_obj, base_args_db_no_masterpwd):
    db_that_do_not_exist = 'I_do_not_exist'
    async with httpx.AsyncClient() as client:
        base_args_db = base_args_db_no_masterpwd(client)
        base_args_obj = base_args_obj(client)
        retval = await db_exist(*base_args_obj[:2], db_name=base_args_obj[2])
        assert retval
        retval = await db_exist(*base_args_obj)
        assert retval
        retval = await db_exist(*base_args_obj, db_name=db_that_do_not_exist)
        assert not retval
        retval = await db_exist(*base_args_db, db_name=db_that_do_not_exist)
        assert not retval
        
        wrong_db_base_args = list(base_args_obj)
        wrong_db_base_args[2] = db_that_do_not_exist
        retval = await db_exist(*wrong_db_base_args)
        assert not retval


@pytest.mark.asyncio
async def test_async_db_list_countries(base_args_db_with_masterpwd):
    async with httpx.AsyncClient() as client:
        base_args = base_args_db_with_masterpwd(client)
        retval = await list_countries(*base_args)
        assert isinstance(retval, list)
        assert len(retval) > 0


@pytest.mark.asyncio
@pytest.mark.auto
async def test_async_db_list_databases(base_args_db_no_masterpwd):
    async with httpx.AsyncClient() as client:
        base_args = base_args_db_no_masterpwd(client)
        retval = await list_databases(*base_args)
        assert isinstance(retval, list)
        assert len(retval) > 0

        for db in retval:
            assert await db_exist(*base_args, db_name=db)


@pytest.mark.asyncio
@pytest.mark.auto
async def test_async_db_list_lang(base_args_db_no_masterpwd):
    async with httpx.AsyncClient() as client:
        base_args = base_args_db_no_masterpwd(client)
        retval = await list_lang(*base_args)
        assert isinstance(retval, list)
        assert len(retval) > 0


@pytest.mark.asyncio
@pytest.mark.auto
async def test_async_db_server_version(base_args_db_no_masterpwd):
    async with httpx.AsyncClient() as client:
        base_args = base_args_db_no_masterpwd(client)
        retval = await server_version(*base_args)
        assert isinstance(retval, str)


@pytest.mark.asyncio
async def test_async_db_change_admin_password(base_args_db_with_masterpwd):
    async with httpx.AsyncClient() as client:
        base_args: Tuple[Any, str, str] = base_args_db_with_masterpwd(client)
        new_passwd = 'admin2'
        countries1 = await list_countries(*base_args)
        assert isinstance(countries1, list)
    
        retval = await change_admin_password(*base_args, new_password=new_passwd)
        assert retval
    
        try:
            # it should work with new password
            countries2 = await list_countries(*base_args[:-1], new_passwd)
            assert isinstance(countries2, list)
            assert countries1 == countries2
        finally:
            try:
                retval = await change_admin_password(*base_args[:-1], new_passwd, new_password=base_args[2])
                assert retval
            except:
                # try again to restore old password
                time.sleep(5)
                retval = await change_admin_password(*base_args[:-1], new_passwd, new_password=base_args[2])
                assert retval


@pytest.mark.asyncio
async def test_async_db_create_rename_duplicate_drop_database(base_args_db_with_masterpwd):
    async with httpx.AsyncClient(http2=True, timeout=5000) as client:
        base_args = base_args_db_with_masterpwd(client)

        alphabet = string.ascii_letters + string.digits
        new_db_name = ''.join(secrets.choice(alphabet) for _ in range(8))
        newest_db_name = ''.join(secrets.choice(alphabet) for _ in range(8))
    
        # create empty database
        retval = await create_database(*base_args,
                                       db_name=new_db_name, demo=False, lang='en',
                                       user_password='test', login='test')
        assert retval
        
        # check if new database exists in two ways
        retval = await list_databases(*base_args)
        assert new_db_name in retval
        assert await db_exist(*base_args, db_name=new_db_name)
    
        # let's test renaming it
        retval = await rename_database(*base_args,
                                       old_name=new_db_name, new_name=newest_db_name)
        assert retval
    
        # check if renaming worked
        retval = await list_databases(*base_args)
        assert new_db_name not in retval
        assert newest_db_name in retval
        assert not await db_exist(*base_args, db_name=new_db_name)
        assert await db_exist(*base_args, db_name=newest_db_name)
        
        # Let's now duplicate the database
        retval = await duplicate_database(*base_args, db_original_name=newest_db_name, db_name=new_db_name)
        assert retval
    
        # Check if now we have both databases
        retval = await list_databases(*base_args)
        assert new_db_name in retval
        assert newest_db_name in retval
        assert await db_exist(*base_args, db_name=new_db_name)
        assert await db_exist(*base_args, db_name=newest_db_name)
        
        # Check migrate, will be a noop probably.
        retval = await migrate_databases(*base_args, databases=[new_db_name, newest_db_name])
        assert retval
        
        # Let's drop both databases
        assert await db_exist(*base_args, db_name=new_db_name)
        retval = await drop_database(*base_args, db_name=new_db_name)
        assert retval
        assert not await db_exist(*base_args, db_name=new_db_name)
    
        assert await db_exist(*base_args, db_name=newest_db_name)
        retval = await drop_database(*base_args, db_name=newest_db_name)
        assert retval
        assert not await db_exist(*base_args, db_name=newest_db_name)
        
        retval = await list_databases(*base_args)
        assert new_db_name not in retval
        assert newest_db_name not in retval


@pytest.mark.asyncio
@pytest.mark.slow
async def test_async_db_dump_database(base_args_db_with_masterpwd):
    async with httpx.AsyncClient(http2=True, timeout=6000) as client:
        base_args = base_args_db_with_masterpwd(client)
        dbs = await list_databases(*base_args)
        db_dump_bytes: bytes
        smallest_dump_len: int = 0
        smallest_db_dump: Optional[bytes] = None
        
        for db in dbs:
            db_dump_bytes = await dump_database(*base_args, db_name=db)
            dump_len = len(db_dump_bytes)
            if dump_len < smallest_dump_len or smallest_dump_len == 0:
                smallest_dump_len = dump_len
                smallest_db_dump = db_dump_bytes
            db_dump = io.BytesIO(db_dump_bytes)
            with zipfile.ZipFile(db_dump, 'r') as zipf:
                assert zipf.testzip() is None
        
        alphabet = string.ascii_letters + string.digits
        new_db_name = ''.join(secrets.choice(alphabet) for _ in range(8))
        retval = await restore_database(*base_args, db_name=new_db_name, data=smallest_db_dump, copy=True)
        assert retval
        
        try:
            assert await db_exist(*base_args, db_name=new_db_name)
        finally:
            retval = await drop_database(*base_args, db_name=new_db_name)
            assert retval
        assert not await db_exist(*base_args, db_name=new_db_name)
