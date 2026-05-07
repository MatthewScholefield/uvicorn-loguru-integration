from pathlib import Path
import sys

import uvicorn

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from uvicorn_loguru_integration import run_uvicorn_loguru


APP_DIR = Path(__file__).resolve().parent


def main() -> None:
    run_uvicorn_loguru(
        uvicorn.Config(
            "example_fastapi_reload.app:app",
            host="127.0.0.1",
            port=8000,
            log_level="info",
            reload=True,
            reload_dirs=[str(APP_DIR)],
        )
    )


if __name__ == "__main__":
    main()
