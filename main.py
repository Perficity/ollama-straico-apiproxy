dotenv_status = "python-dotenv unavailable; skipping .env load"
dotenv_log_level = "info"

try:
    from dotenv import load_dotenv
except ImportError:
    pass
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

from app import app, logging, log_level
from api_endpoints import lm_studio, ollama, claude
import view

import uvicorn

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.info("Starting the web server")
    if dotenv_log_level == "warning":
        logger.warning(dotenv_status)
    else:
        logger.info(dotenv_status)
    is_debug = log_level in ["INFO", "DEBUG"]
    HOST = environ.get("HOST", "0.0.0.0")
    PORT = int(environ.get("PORT", "3214"))
    uvicorn.run(app, host=HOST, port=PORT, log_level=log_level.lower())
