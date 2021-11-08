from pydantic import BaseSettings, Field
import logging


DEFAULT_LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(asctime)s # %(name)s # FRM: %(levelprefix)s %(message)s",
                "datefmt": "%Y/%m/%d %I:%M:%S",
                "use_colors": True,
            },
            "application": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(asctime)s # %(name)s # APP: %(levelprefix)s %(message)s",
                "datefmt": "%Y/%m/%d %I:%M:%S",
                "use_colors": True,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": '%(asctime)s # %(name)s # ACS: %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
                "datefmt": "%Y/%m/%d %I:%M:%S",
                "use_colors": True,
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "application": {
                "formatter": "application",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "error": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
                "level": "INFO"
            },
        },
        "loggers": {
            "default":{"handlers":["default"], "level": logging.INFO},
            "fastapi":{"handlers":["default"], "level": logging.INFO},
            "application": {"handlers": ["application"], "level": logging.INFO},
            "uvicorn": {"handlers": ["default"], "level": logging.INFO, "propagate": False},
            "uvicorn.error": {"handlers": ["error"], "level": logging.INFO, "propagate": False},
            "uvicorn.access": {"handlers": ["access"], "level": logging.INFO, "propagate": False}
        },
    }

class LoggingConfigModel(BaseSettings):
    level: str = Field(default="debug")
    config: dict = Field(default=DEFAULT_LOGGING_CONFIG)
