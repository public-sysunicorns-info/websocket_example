
import uvicorn
import logging
import ssl

from application import Application
from application.config import ApplicationConfigModel

logger = logging.getLogger(__package__)


if __name__ == "__main__":

    _application_config = ApplicationConfigModel()

    try:
        uvicorn.run(
            app="main:application",
            host=_application_config.server_host,
            port=_application_config.server_port,
            workers=_application_config.uvicorn_config.worker_count,
            log_level=_application_config.logging_config.level,
            log_config=_application_config.logging_config.config,
            lifespan="on",
            loop="uvloop",
            ws="auto",
#            ssl_ca_certs=_application_config.ssl_config.ca_path,
#            ssl_keyfile=_application_config.ssl_config.key_path,
#            ssl_certfile=_application_config.ssl_config.crt_path,
#            ssl_cert_reqs=ssl.CERT_REQUIRED
        )
    except SystemExit as e:
        logger.critical(msg="Application Crash on uvicorn.run")
else:
    application = Application()
