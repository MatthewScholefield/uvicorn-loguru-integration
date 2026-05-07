from typing import Optional, Type
import functools
import logging

import uvicorn
from loguru_logging_intercept import setup_loguru_logging_intercept
from uvicorn.supervisors import ChangeReload, Multiprocess

UVICORN_LOGGING_MODULES = ("uvicorn.error", "uvicorn.asgi", "uvicorn.access")


def _run_server_with_intercept(config: uvicorn.Config, force_exit=False, **kwargs):
    setup_loguru_logging_intercept(
        level=_get_log_level(config), modules=UVICORN_LOGGING_MODULES
    )
    server = uvicorn.Server(config=config)
    server.force_exit = force_exit
    server.run(**kwargs)


def run_uvicorn_loguru(config: uvicorn.Config, force_exit=False):
    """Same as uvicorn.run but injects loguru logging"""

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
        return logging.getLevelName(config.log_level)
    else:
        return config.log_level or logging.INFO


def _get_supervisor_type(config: uvicorn.Config) -> Optional[Type]:
    if config.should_reload:
        return ChangeReload
    if config.workers > 1:
        return Multiprocess
    return None
