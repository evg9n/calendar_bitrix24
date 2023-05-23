import fast_bitrix24
from send_whatsapp import send_whatsapp
from config import TOKEN, CHANNEL_ID, PHONE
from logging import getLogger
from utils import set_json_data_id, get_json_data_id


logger = getLogger('bitrix24')


def get_data_event(hook: str, meet_id: int) -> None:

    logger.debug("Функция get_data_event")
    bx24 = fast_bitrix24.Bitrix(hook)
    affairs = bx24.get_all(method='calendar.event.getbyid',
                           params={'id': meet_id})

    name = affairs["NAME"]
    date_from = f'{affairs["DATE_FROM"][:-3]}({affairs["TZ_FROM"]})'
    date_to = f'{affairs["DATE_TO"][:-3]}({affairs["TZ_TO"]})'
    discription = affairs["DESCRIPTION"]

    data = get_json_data_id()
    data[meet_id] = dict(name=name, date_from=date_from, date_to=date_to, discription=discription)
    set_json_data_id(data)

    # Шаблон сообщения
    message = f"""
❗Новая встреча❗
{name}
{discription}
{date_from}
{date_to}
"""
    response = send_whatsapp(token=TOKEN, channel_id=CHANNEL_ID, phone=PHONE, text=message)

    if response.status_code != 201:
        logger.error(f'status code {response.status_code}')
    else:
        logger.debug(response.status_code)


def get_data_event_false(meet_id):
    data = get_json_data_id()
    meet = data.get(meet_id)
    if meet is None:
        message = "Отмена встречи❗" \
                  "\nИнформация  о встрече отсутствует"
    else:
        message = f"""
❗Отмена встречи❗
{meet.get('name')}
{meet.get('discription')}
{meet.get('date_from')}
{meet.get('date_to')}
        """
        data.pop(meet_id)
        set_json_data_id(data)

    response = send_whatsapp(token=TOKEN, channel_id=CHANNEL_ID, phone=PHONE, text=message)

    if response.status_code != 201:
        logger.error(f'status code {response.status_code}')
    else:
        logger.debug(response.status_code)


def check_affairs(webhook: str, owner_id: int, now: str, future: str, list_id: list):
    logger.debug("Функция check_affairs")
    bx24 = fast_bitrix24.Bitrix(webhook)
    affairs = bx24.get_all(method='calendar.event.get',
                           params={'type': 'user',
                                   'ownerId': owner_id,
                                   'from': now,
                                   'to': future})
    result_meet_id = list()

    for event in affairs:
        logger.debug(event)
        meet_id = event['ID']
        result_meet_id.append(meet_id)

        # 'MEETING_STATUS': 'Y'
        if event.get('MEETING_STATUS') == 'Y' and meet_id not in list_id:
            print(event)
            logger.info('Новая встреча')
            get_data_event(hook=webhook, meet_id=meet_id)

            list_id.append(meet_id)

        elif event.get('MEETING_STATUS') == 'N' and meet_id in list_id:
            logger.info('Отмена встречи')

            get_data_event_false(meet_id)

            # get_data_event(hook=webhook, meet_id=meet_id, active=False)

            list_id.remove(meet_id)

    for meet_id in list_id:
        if meet_id not in result_meet_id:
            logger.info('Отмена встречи')

            get_data_event_false(meet_id)

            list_id.remove(meet_id)

    logger.info(f'Функция check_affairs возвращает {list_id}')
    return list_id
