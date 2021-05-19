import nox
import nox_poetry
import io
import toml
from typing import List

nox.options.reuse_existing_virtualenvs = True
nox.options.pythons = ("3.8", "3.9")
MAIN_PYTHON = "3.9"
nox.options.sessions = ("update", "before", "black",
                        "lint", "safety", "after",)
locations = ("aio_odoorpc_base", "tests", "noxfile.py")


@nox_poetry.session(python=nox.options.pythons)
def update(session):
    session.run("rm", "poetry.lock", "requirements.txt", "dev-requirements.txt", success_codes=[0, 1])
    session.run("poetry", "update")


@nox_poetry.session(python=False)
def before(session):
    gen_sync_code()
    
    with io.open('pyproject.toml', 'rt') as f:
        pyproj = toml.load(f)

    nox.options.pythons = pyproj["tool"]["pyenv"]["python-version"]
    session.run("pyenv", "local", *nox.options.pythons)

    flk8 = pyproj["tool"].copy()
    keys_to_del: List[str] = [k for k in flk8 if not k.startswith("flake8")]
    k: str
    for k in keys_to_del:
        del flk8[k]
    flk8 = toml.dumps(flk8)
    flk8 = flk8.replace('"', "").replace(", ", ",")

    with io.open('.flake8', 'wt') as f:
        f.write(flk8)


@nox_poetry.session(python=False)
def black(session):
    session.run("black", ".")


@nox_poetry.session(python=False)
def lint(session):
    args = session.posargs or locations
    session.run("flake8", *args)


@nox_poetry.session(python=False)
def safety(session):
    import tempfile
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox_poetry.session(python=nox.options.pythons)
def tests(session):
    session.run("poetry", "update", external=True)
    session.run("pytest", "--cov")


@nox_poetry.session(python=False)
def after(session):
    files_to_delete = ["poetry.lock", "requirements.txt", "dev-requirements.txt", ".coverage"]
    dirs_to_delete = ["__pycache__", ".pytest_cache"]
    for f in files_to_delete:
        session.run("rm", f, success_codes=[0, 1])
    for d in dirs_to_delete:
        session.run("rm", "-Rf", d, success_codes=[0, 1])


def gen_sync_code():
    files: List[tuple[str, str]] = [('aio_odoorpc_base/aio/__init__.py', 'aio_odoorpc_base/sync/__init__.py'),
                                     ('aio_odoorpc_base/aio/rpc.py', 'aio_odoorpc_base/sync/rpc.py'),
                                     ('aio_odoorpc_base/aio/common.py', 'aio_odoorpc_base/sync/common.py'),
                                     ('aio_odoorpc_base/aio/db.py', 'aio_odoorpc_base/sync/db.py'),
                                     ('aio_odoorpc_base/aio/object.py', 'aio_odoorpc_base/sync/object.py'),
                                     ('tests/test_async_common.py', 'tests/test_sync_common.py'),
                                     ('tests/test_async_db.py', 'tests/test_sync_db.py'),
                                     ('tests/test_async_object.py', 'tests/test_sync_object.py')]
    delete_lines: list[str] = ['from inspect import isawaitable',
                                'if isawaitable(data):',
                                'data = await data',
                                '@pytest.mark.asyncio']
    comment_lines: list[str] = []
    repl: list[tuple[str, str]] = [('from aio_odoorpc_base.aio', 'from aio_odoorpc_base.sync'),
                                    ('T_AsyncResponse', 'T_Response'),
                                    ('T_AsyncHttpClient', 'T_HttpClient'),
                                    ('async def', 'def'),
                                    ('async with', 'with'),
                                    ('httpx.AsyncClient', 'httpx.Client'),
                                    ('async_base_args', 'base_args'),
                                    ('test_async_', 'test_sync_'),
                                    ('asyncio.create_task(execute_kw(**exkw_kwargs))', 'execute_kw(**exkw_kwargs)'),
                                    ('await ', '')]

    f: tuple[str, str]
    for f in files:
        filename_async = f[0]
        filename_sync = f[1]
        import os
        dt_mod_async = os.path.getmtime(filename_async)
        dt_mod_script = os.path.getmtime(__file__)
        try:
            dt_mod_sync = os.path.getmtime(filename_sync)
        except OSError:
            dt_mod_sync = 0

        if dt_mod_async < dt_mod_sync and dt_mod_script < dt_mod_sync:
            return

        lines: list[str] = []
        with open(filename_async, 'rt') as file:
            for line in file:
                line_s: str = line.strip()
                keep: bool = True
                for t in delete_lines:
                    if t == line_s:
                        print(f'Deleted line: {t}')
                        keep = False
                        break
                if keep:
                    lines.append(line)

        f_sync: str = ''.join(lines)
        t: tuple[str, str]
        index: int
        for t in repl:
            index = f_sync.find(t[0])
            if index >= 0:
                f_sync = f_sync.replace(t[0], t[1])
            else:
                print(f'No match for rule: {t[0]} -> {t[1]}')

        with open(filename_sync, 'w') as file:
            file.write(f_sync)

