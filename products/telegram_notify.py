import requests
from django.conf import settings

def notify_telegram(user):
    from accounts.models import CustomUser
    user = CustomUser.objects.get(pk=user.pk)

    if not user.telegram_id:
        print(f"❌ У пользователя {user.phone} нет telegram_id. Уведомление не отправлено.")
        return

    print(f"✅ Отправляем сообщение пользователю {user.phone} (telegram_id: {user.telegram_id})")
    print(f"telegram_id: {user.telegram_id}")
    print(f"BOT_TOKEN: {settings.BOT_TOKEN}")

    if user.telegram_id:
        print(f"✅ Найден пользователь: {user.phone}, telegram_id = {user.telegram_id}")
        msg = "Вам пришёл новый заказ!"
        token = settings.BOT_TOKEN
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        response = requests.post(url, data={
            'chat_id': user.telegram_id,
            'text': msg
        })
        print(f"[DEBUG] Telegram API ответ: {response.status_code} — {response.text}")


# import requests
# from django.conf import settings
#
# def notify_telegram(user):
#     print(f"telegram_id: {user.telegram_id}")
#     print(f"BOT_TOKEN: {settings.BOT_TOKEN}")
#
#     if user.telegram_id:
#         print(f"✅ Найден пользователь: {user.phone}, сохраняем telegram_id = {telegram_id}")
#         msg = "Вам пришёл новый заказ!"
#         token = settings.BOT_TOKEN
#         url = f"https://api.telegram.org/bot{token}/sendMessage"
#         requests.post(url, data={
#             'chat_id': user.telegram_id,
#             'text': msg
#         })

# import os
# import requests
# from dotenv import load_dotenv
#
# load_dotenv()
#
# def notify_telegram(user):
#
#
#
#
#     if user.telegram_id:
#         msg = "Вам пришёл новый заказ!"
#         token = os.getenv("BOT_TOKEN")
#         url = f"https://api.telegram.org/bot{token}/sendMessage"
#         response = requests.post(url, data={
#             'chat_id': user.telegram_id,
#             'text': msg
#         })
#         print("Telegram response:", response.status_code, response.text)
