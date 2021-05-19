from invoke import task, call
import io
import toml


@task
def clean(c, all=False, docs=False, bytecode=False, requirements=False, poetry_lock=False,
          build=False, flake8=False, pyenv=False, others=False, extras: list = None):
    patterns = list()
    if docs or all:
        patterns.append('docs/_build')
    if bytecode or all:
        patterns.append('**/*.pyc')
    if requirements or all:
        patterns.extend(('requirements.txt', 'dev-requirements.txt'))
    if poetry_lock or all:
        patterns.append('poetry.lock')
    if build or all:
        patterns.append('build')
    if flake8 or all:
        patterns.append('.flake8')
    if pyenv or all:
        patterns.append('.python-version')
    if others or all:
        patterns.extend(('**/*.swp', '.coverage', '.benchmark', '__pycache__', '.pytest_cache'))
    if extras:
        patterns.extend(extras)
    
    for pattern in patterns:
        c.run(f"rm -rf {pattern}")


@task(pre=[call(clean, requirements=True, poetry_lock=True)])
def update(c):
    c.run("poetry", "update")


@task
def commit(c, major: bool = False, minor: bool = False, patch: bool = False):
    
    if major:
        bump = "major"
    elif minor:
        bump = "minor"
    elif patch:
        bump = "patch"
    else:
        raise RuntimeError('Is this a major, minor or patch release?')

    c.run(f"poetry version {bump}")
    c.run("git add .")
    

@task
def gen_cfg_files(c, pyenv: bool = False, flake8: bool = False):
    with io.open('pyproject.toml', 'rt') as f:
        pyproj = toml.load(f)
    
    if pyenv:
        python_versions: list = pyproj["tool"]["pyenv"]["python-version"]
        c.run("pyenv", "local", *python_versions)
    
    if flake8:
        flk8: dict = pyproj["tool"].copy()
        keys_to_del: list[str] = [k for k in flk8 if not k.startswith("flake8")]
        k: str
        for k in keys_to_del:
            del flk8[k]
        flk8_txt: str = toml.dumps(flk8)
        flk8_txt = flk8_txt.replace('"', "").replace(", ", ",")
    
        with io.open('.flake8', 'wt') as f:
            f.write(flk8_txt)


@task
def gen_sync_code(c):
    files: list[tuple[str, str]] = [('aio_odoorpc_base/aio/__init__.py', 'aio_odoorpc_base/sync/__init__.py'),
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
