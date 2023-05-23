# Инструкция

Нужно создать файл config.py и заполнить следующими данными:
 + TOKEN - ключ API Wazzup
 + CHANNEL_ID - id канала Wazzup можно взять из url на канал 
 + PHONE - номер на который нужно отправлять уведомления в whatsapp формата 70123456789
 + WEBHOOK - Входящий вебхук bitrix24 с правами на календарь
 + OWNER_ID - id пользователя bitrix24, натуральное число
 + FUTURE_DAYS - на сколько дней вперед проверять, натуральное число
 + SLEEP_SECONDS - интервал между запросами в секундах, натуральное число указывает время в секундах

Пример содержимого файла:
```python
TOKEN = 'TOKEN'
CHANNEL_ID = "CHANNEL_ID"
PHONE = "PHONE"

WEBHOOK = "WEBHOOK"
OWNER_ID = 0
SLEEP_SECONDS = 30
FUTURE_DAYS = 14
```