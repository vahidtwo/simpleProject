from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

logs = ["accounts",]
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {message} \n",
            "style": "{",
        }
    },
    "handlers": {
        "console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "verbose"},
        "logger_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "verbose",
            "filename": f"{BASE_DIR}/var/logs/django.log",
        }
    },
    "loggers": {
        "django": {
            "handlers": ["logger_file", "console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
for log in logs:
    LOGGING["handlers"].update(
        {
            log: {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "formatter": "verbose",
                "filename": f"{BASE_DIR}/var/logs/{log}.log",
            }
        }
    )
    LOGGING["loggers"].update({log: {"handlers": [log], "level": "INFO"}})
