dotenv_status = "python-dotenv unavailable; skipping .env load"
dotenv_log_level = "info"

try:
    from dotenv import load_dotenv
except ImportError:
    pass
import importlib.util
import platform
else:
    try:
        dotenv_found = load_dotenv()
        dotenv_status = (
            ".env loaded via python-dotenv"
            if dotenv_found
            else "python-dotenv available; no .env file loaded"
        )
    except Exception as exc:
        dotenv_status = f"Failed to load .env via python-dotenv: {exc}"
        dotenv_log_level = "warning"

from os import environ
import platform
from importlib.util import find_spec

import uvicorn


def build_uvicorn_kwargs(host: str, port: int, runtime_log_level: str) -> dict:
    kwargs = {
        "host": host,
        "port": port,
        "log_level": runtime_log_level.lower(),
    }

    if platform.system() == "Darwin":
        if importlib.util.find_spec("uvloop") is not None:
            kwargs["loop"] = "uvloop"
        if importlib.util.find_spec("httptools") is not None:
            kwargs["http"] = "httptools"

    return kwargs


if __name__ == "__main__":
    from app import app, logging, log_level
    from api_endpoints import lm_studio, ollama, claude
    import view

    logger = logging.getLogger(__name__)
    logger.info("Starting the web server")
    if dotenv_log_level == "warning":
        logger.warning(dotenv_status)
    else:
        logger.info(dotenv_status)
    is_debug = log_level in ["INFO", "DEBUG"]
    HOST = environ.get("HOST", "0.0.0.0")
    PORT = int(environ.get("PORT", "3214"))
    uvicorn.run(app, **build_uvicorn_kwargs(HOST, PORT, log_level))
    uvicorn_kwargs = {
        "host": HOST,
        "port": PORT,
        "log_level": log_level.lower(),
    }

    # Optimize default runtime settings for local macOS usage.
    if platform.system() == "Darwin":
        if find_spec("uvloop") is not None:
            uvicorn_kwargs["loop"] = "uvloop"
        if find_spec("httptools") is not None:
            uvicorn_kwargs["http"] = "httptools"

    uvicorn.run("main:app", **uvicorn_kwargs)
