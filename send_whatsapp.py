import requests
from requests.models import Response
from logging import getLogger


logger = getLogger('send_whatsapp')


def send_whatsapp(token: str, channel_id: str, phone: str, text: str) -> Response:
    logger.debug('Функция send_whatsapp')
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "channelId": channel_id,
        "chatType": "whatsapp",
        "chatId": phone,
        "text": text
    }
    url = "https://api.wazzup24.com/v3/message"

    response = requests.post(url=url, json=data, headers=headers)

    logger.info(f'Результат запроса {response}')

    return response
