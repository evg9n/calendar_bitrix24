import datetime
from datetime import datetime as dt
from re import match
import re
import os
from json import load, dump
from logging import getLogger
from datetime import timedelta, datetime


logger = getLogger('utils')


def datetime_now() -> str:
    """
    Определяет текущую дату и время без миллисекунд с минусом 2 часа, возвращает str
    """
    logger.debug('функция datetime_now')
    pattern = r"(\d{4}-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}))"
    now = str(dt.now() - timedelta(hours=3))
    now = match(pattern=pattern, string=now)
    if now:
        logger.info(f'функция datetime_now возвращает {now.group()}')
        return now.group()
    else:
        # todo изменить
        logger.info(f'функция datetime_now возвращает None')
        return ''


def datetime_future(days: int) -> str:
    """
    Определяет будущую дату и время без миллисекунд, возвращает str
    """
    logger.debug('функция datetime_now')
    pattern = r"(\d{4}-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}))"
    date = str(dt.now() + timedelta(days=days))
    date = match(pattern=pattern, string=date)
    if date:
        logger.info(f'функция datetime_now возвращает {date.group()}')
        return date.group()
    else:
        # todo изменить
        logger.info(f'функция datetime_now возвращает None')
        return ''


def check_date(date: str):
    # "30.05.2023 14:35(Europe/Moscow)"

    pattern_date = r"\d{2}.\d{2}.\d{4}"
    pattern_time = r"\d{2}:\d{2}"
    result_date = re.search(pattern_date, date)
    result_time = re.search(pattern_time, date)

    if result_date and result_time:
        result_date = result_date.group()
        result_time = result_time.group()

        day, month, year = str(result_date).split('.')
        hour, minute = str(result_time).split(':')

        res = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute))
        now = datetime.now()

        if res > now:
            return False

    return True


def get_json_data_id():
    logger.debug('Функция get_json_data_id')
    file = 'data_id.json'

    if file in os.listdir():
        with open(file, 'r', encoding='utf-8') as file:
            result = load(file)
        return result
    else:
        return dict()


def set_json_data_id(data_id) -> None:
    logger.debug('функция set_json')
    with open('data_id.json', 'w', encoding='utf-8') as file:
        dump(data_id, file, ensure_ascii=False, indent=4)


def get_json():
    """
    Получить данные из json файла
    """
    logger.debug('функция get_json')
    file = 'list_id.json'
    if file in os.listdir():
        with open(file, 'r', encoding='utf-8') as file:
            result = load(file)
        logger.info(f'функция get_json возвращает {result}')
        return result
    else:
        logger.info(f'функция get_json возвращает пустой список')
        return list()


def set_json(list_id) -> None:
    """
    Записать данные в json файл
    """
    logger.debug('функция set_json')
    with open('list_id.json', 'w', encoding='utf-8') as file:
        dump(list_id, file, ensure_ascii=False, indent=4)
