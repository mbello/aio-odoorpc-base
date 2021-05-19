import pytest
import httpx
from aio_odoorpc_base.aio.common import about, authenticate, login, set_loglevel, version


@pytest.mark.asyncio
@pytest.mark.auto
async def test_async_common_about(base_args_common):
    async with httpx.AsyncClient() as client:
        base_args = base_args_common(client)
        retval = await about(*base_args, extended=True)
        assert isinstance(retval, list)
        assert len(retval) == 2
        assert isinstance(retval[0], str) and isinstance(retval[1], str)
        
        retval = await about(*base_args, extended=False)
        assert isinstance(retval, str)

        retval = await about(*base_args)
        assert isinstance(retval, str)


@pytest.mark.asyncio
@pytest.mark.auto
async def test_async_common_login_authenticate(base_args_common):
    async with httpx.AsyncClient() as client:
        base_args = base_args_common(client)
        retval_login = await login(*base_args)
        assert isinstance(retval_login, int)
        retval_authenticate = await authenticate(*base_args)
        assert isinstance(retval_authenticate, int)
        assert retval_login == retval_authenticate

        retval = await login(*base_args[:-1], 'wrong_password')
        assert retval is False
        retval = await authenticate(*base_args[:-1], 'wrong_password')
        assert retval is False


@pytest.mark.asyncio
@pytest.mark.auto
async def test_async_common_set_loglevel(base_args_common):
    async with httpx.AsyncClient() as client:
        base_args = base_args_common(client)
        retval = await set_loglevel(*base_args, loglevel=5)
        assert isinstance(retval, bool)


@pytest.mark.asyncio
@pytest.mark.auto
async def test_async_common_version(base_args_common):
    async with httpx.AsyncClient() as client:
        base_args = base_args_common(client)
        retval = await version(*base_args)
        assert retval
        assert isinstance(retval, dict)
