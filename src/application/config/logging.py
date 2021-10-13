from pydantic import BaseSettings, Field


DEFAULT_LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(asctime)s # FRM: %(levelprefix)s %(message)s",
                "datefmt": "%Y/%m/%d %I:%M:%S",
                "use_colors": None,
            },
            "application": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(asctime)s # APP: %(levelprefix)s %(message)s",
                "datefmt": "%Y/%m/%d %I:%M:%S",
                "use_colors": None,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": '%(asctime)s # ACS: %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
                "datefmt": "%Y/%m/%d %I:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "application": {
                "formatter": "application",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "application": {"handlers": ["application"], "level": "DEBUG"},
            "uvicorn": {"handlers": ["default"], "level": "INFO"},
            "uvicorn.error": {"level": "INFO"},
            "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
        },
    }

class LoggingConfigModel(BaseSettings):
    level: str = Field(default="debug")
    config: dict = Field(default=DEFAULT_LOGGING_CONFIG)
