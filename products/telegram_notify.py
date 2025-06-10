import requests
from django.conf import settings

def notify_telegram(user):
    from accounts.models import CustomUser
    user = CustomUser.objects.get(pk=user.pk)

    if not user.telegram_id:
        print(f"❌ У пользователя {user.phone} нет telegram_id. Уведомление не отправлено.")
        return



    if user.telegram_id:

        msg = "Вам пришёл новый заказ!"
        token = settings.BOT_TOKEN
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        response = requests.post(url, data={
            'chat_id': user.telegram_id,
            'text': msg
        })
        print(f"[DEBUG] Telegram API ответ: {response.status_code} — {response.text}")


