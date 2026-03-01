try:
    from dotenv import load_dotenv

    load_dotenv()
except:
    pass
from importlib.util import find_spec
from os import environ
import platform
from importlib.util import find_spec

from app import app, logging, log_level
from api_endpoints import lm_studio, ollama, claude
import view

import uvicorn

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.info("Starting the web server")
    HOST = environ.get("HOST", "0.0.0.0")
    PORT = int(environ.get("PORT", "3214"))

    uvicorn_kwargs = {
        "host": HOST,
        "port": PORT,
        "log_level": log_level.lower(),
    }

    # Optional local runtime optimizations. uvicorn will use these when present.
    if find_spec("uvloop") is not None:
        uvicorn_kwargs["loop"] = "uvloop"

    if find_spec("httptools") is not None:
        uvicorn_kwargs["http"] = "httptools"

    uvicorn.run(app, **uvicorn_kwargs)
    # Optimize default runtime settings for local macOS usage.
    if platform.system() == "Darwin":
        if find_spec("uvloop") is not None:
            uvicorn_kwargs["loop"] = "uvloop"
        if find_spec("httptools") is not None:
            uvicorn_kwargs["http"] = "httptools"

    uvicorn.run("main:app", **uvicorn_kwargs)
