from time import sleep
from utils import get_json, set_json, datetime_now
from bitrix24 import check_affairs
from config import WEBHOOK, OWNER_ID, SLEEP_SECONDS
from logging.config import dictConfig
from logging import getLogger, INFO


FORMAT = "%(levelname)-8s [%(asctime)s] %(message)s"
datefmt = '%d.%m.%y %H:%M:%S'

level = INFO

log_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standart': {
            'format': FORMAT,
            'datefmt': datefmt
        }

    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': level,
            'formatter': 'standart',
            'stream': 'ext://sys.stdout'
        },
        'file_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': level,
            'filename': "logs/log.log",
            'encoding': 'utf-8',
            'when': 'D',
            'interval': 1,
            'backupCount': 500,
            'formatter': 'standart'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file_handler', 'console'],
            'level': level
        },
        'send_whatsapp': {
            'handlers': ['file_handler', 'console'],
            'level': level
        },
        'bitrix24': {
            'handlers': ['file_handler', 'console'],
            'level': level
        },
        'utils': {
            'handlers': ['file_handler', 'console'],
            'level': level
        }
    }
}

dictConfig(log_config)
logger = getLogger()


if __name__ == "__main__":
    logger.info('start')

    while True:
        try:
            list_id = get_json()
            now = datetime_now()
            list_id = check_affairs(webhook=WEBHOOK, owner_id=OWNER_ID, now=now, list_id=list_id)
            set_json(list_id)
            sleep(SLEEP_SECONDS)
        except Exception as error :
            logger.error(f'{error}')
            break
