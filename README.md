# Uvicorn Loguru Integration

*Code to integrate
[uvicorn.run](https://github.com/encode/uvicorn/blob/master/uvicorn/main.py#L365) with
[Loguru](https://github.com/Delgan/loguru) logging*

[Loguru](https://github.com/Delgan/loguru) is a great alternative logging library for
Python. However, since [Uvicorn](https://www.uvicorn.org/) uses Python's standard
logging library, using Loguru looks inconsistent. This module injects an intercept
handler in the correct location after initializing Uvicorn so that all logs get routed
through Loguru.

## Usage

Call `run_uvicorn_loguru` with an instance of `uvicorn.Config`:

```python
from uvicorn_loguru_integration import run_uvicorn_loguru


def main():
    run_uvicorn_loguru(
        uvicorn.Config(
            "myapp:app",
            host="0.0.0.0",
            port=8000,
            log_level="info",
            reload=True,
        )
    )


if __name__ == "__main__":
    main()
```

## Installation

Install via `pip`:

```bash
pip3 install uvicorn-loguru-integration
```
