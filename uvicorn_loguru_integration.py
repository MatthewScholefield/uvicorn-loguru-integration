from typing import Optional, Type
import functools
import logging

import uvicorn
from loguru_logging_intercept import setup_loguru_logging_intercept
from uvicorn.supervisors import ChangeReload, Multiprocess

UVICORN_LOGGING_MODULES = ("uvicorn.error", "uvicorn.asgi", "uvicorn.access")


def _setup_loguru_intercept(level: int):
    setup_loguru_logging_intercept(level=level, modules=UVICORN_LOGGING_MODULES)


def _run_server_with_intercept(config: uvicorn.Config, force_exit=False, **kwargs):
    _setup_loguru_intercept(_get_log_level(config))
    server = uvicorn.Server(config=config)
    server.force_exit = force_exit
    server.run(**kwargs)


def run_uvicorn_loguru(config: uvicorn.Config, force_exit=False):
    """Same as uvicorn.run but injects loguru logging"""

    _setup_loguru_intercept(_get_log_level(config))

    supervisor_type = _get_supervisor_type(config)
    if supervisor_type:
        sock = config.bind_socket()
        supervisor = supervisor_type(
            config,
            target=functools.partial(
                _run_server_with_intercept,
                config,
                force_exit=force_exit,
            ),
            sockets=[sock],
        )
        supervisor.run()
    else:
        _run_server_with_intercept(config, force_exit=force_exit)


def _get_log_level(config: uvicorn.Config) -> int:
    if isinstance(config.log_level, str):
        return logging._nameToLevel.get(config.log_level.upper(), logging.INFO)
    else:
        return config.log_level or logging.INFO


def _get_supervisor_type(config: uvicorn.Config) -> Optional[Type]:
    if config.should_reload:
        return ChangeReload
    if config.workers > 1:
        return Multiprocess
    return None
