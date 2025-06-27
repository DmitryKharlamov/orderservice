import telebot
from django.conf import settings
from accounts.models import CustomUser

def notify_telegram(user):
    if not user.telegram_id:
        print(f"❌ У пользователя {user.phone} нет telegram_id. Уведомление не отправлено.")
    bot = telebot.TeleBot(settings.BOT_TOKEN)
    msg = "Вам пришёл новый заказ!"

    try:
        bot.send_message(chat_id=user.telegram_id, text=msg)
        print(f"✅ Уведомление отправлено пользователю {user.phone}")
    except Exception as e:
        print(f"❌ Ошибка при отправке сообщения: {e}")
