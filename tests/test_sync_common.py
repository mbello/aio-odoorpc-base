import pytest
import httpx
from aio_odoorpc_base.sync.common import about, authenticate, login, set_loglevel, version


@pytest.mark.auto
def test_sync_common_about(base_args_common):
    with httpx.Client() as client:
        base_args = base_args_common(client)
        retval = about(*base_args, extended=True)
        assert isinstance(retval, list)
        assert len(retval) == 2
        assert isinstance(retval[0], str) and isinstance(retval[1], str)

        retval = about(*base_args, extended=False)
        assert isinstance(retval, str)

        retval = about(*base_args)
        assert isinstance(retval, str)


@pytest.mark.auto
def test_sync_common_login_authenticate(base_args_common):
    with httpx.Client() as client:
        base_args = base_args_common(client)
        retval_login = login(*base_args)
        assert isinstance(retval_login, int)
        retval_authenticate = authenticate(*base_args)
        assert isinstance(retval_authenticate, int)
        assert retval_login == retval_authenticate

        retval = login(*base_args[:-1], 'wrong_password')
        assert retval is False
        retval = authenticate(*base_args[:-1], 'wrong_password')
        assert retval is False


@pytest.mark.auto
def test_sync_common_set_loglevel(base_args_common):
    with httpx.Client() as client:
        base_args = base_args_common(client)
        retval = set_loglevel(*base_args, loglevel=5)
        assert isinstance(retval, bool)


@pytest.mark.auto
def test_sync_common_version(base_args_common):
    with httpx.Client() as client:
        base_args = base_args_common(client)
        retval = version(*base_args)
        assert retval
        assert isinstance(retval, dict)
