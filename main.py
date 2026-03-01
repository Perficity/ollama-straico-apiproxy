try:
    from dotenv import load_dotenv

    load_dotenv()
except:
    pass
import importlib.util
import platform
from os import environ

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
    is_debug = log_level in ["INFO", "DEBUG"]
    HOST = environ.get("HOST", "0.0.0.0")
    PORT = int(environ.get("PORT", "3214"))
    uvicorn.run(app, **build_uvicorn_kwargs(HOST, PORT, log_level))
