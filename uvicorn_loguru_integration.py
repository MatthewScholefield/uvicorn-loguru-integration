import uvicorn
from loguru_logging_intercept import setup_loguru_logging_intercept
import logging
from uvicorn.supervisors import Multiprocess, ChangeReload


UVICORN_LOGGING_MODULES = ("uvicorn.error", "uvicorn.asgi", "uvicorn.access")


def run_uvicorn_loguru(config: uvicorn.Config):
    """Same as uvicorn.run but injects loguru logging"""
    server = uvicorn.Server(config=config)
    setup_loguru_logging_intercept(
        level=logging.getLevelName(config.log_level.upper()),
        modules=UVICORN_LOGGING_MODULES
    )
    supervisor_type = None
    if config.should_reload:
        supervisor_type = ChangeReload
    if config.workers > 1:
        supervisor_type = Multiprocess
    if supervisor_type:
        sock = config.bind_socket()
        supervisor = supervisor_type(config, target=server.run, sockets=[sock])
        supervisor.run()
    else:
        server.run()
