import os
import sys
import logging
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Добавляем путь к корню проекта, если нужно (опционально)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Загрузка переменных окружения
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
from bot.models import CustomUser  # Импорт SQLAlchemy модели, которую ты должен создать
from bot.models import Base  # если нужно будет создавать таблицы

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите ваш номер телефона (в формате +71234567890):")
    context.user_data["awaiting_phone"] = True


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = Session()
    phone = update.message.text.strip()
    telegram_id = update.effective_user.id

    if context.user_data.get("awaiting_phone"):
        try:
            user = session.query(CustomUser).filter_by(phone=phone).first()
            if user:
                user.telegram_id = str(telegram_id)
                session.commit()
                await update.message.reply_text("Вы успешно зарегистрированы в системе!")
            else:
                await update.message.reply_text("Пользователь с таким номером не найден.")
        except Exception as e:
            logging.error(f"Ошибка при обработке сообщения: {e}")
            await update.message.reply_text("Произошла ошибка. Попробуйте позже.")
        finally:
            context.user_data["awaiting_phone"] = False
            session.close()


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()


if __name__ == "__main__":
    main()

#
#
# import sys
# import os
#
# # Добавляем путь к корню проекта (где manage.py, config и accounts)
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#
# import logging
# import asyncio
# from telegram import Update
# from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from dotenv import load_dotenv
#
# # Загрузка переменных окружения
# load_dotenv()
#
# # Настройка Django окружения
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# import django
# django.setup()
#
# from accounts.models import CustomUser
#
#
# # Загрузка переменных окружения
# load_dotenv()
#
# # Настройка Django окружения
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Замените OrderService на имя вашего проекта
# django.setup()
#
# # Теперь можно импортировать модели Django
# from accounts.models import CustomUser
#
# from accounts.models import CustomUser
# load_dotenv()
#
# BOT_TOKEN = os.getenv("BOT_TOKEN")
# DATABASE_URL = os.getenv("DATABASE_URL")
#
# logging.basicConfig(level=logging.INFO)
#
# engine = create_engine(DATABASE_URL)
# Session = sessionmaker(bind=engine)
#
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Введите ваш номер телефона (в формате +71234567890):")
#     context.user_data["awaiting_phone"] = True
#
# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     session = Session()
#     phone = update.message.text.strip()
#     telegram_id = update.effective_user.id
#
#     if context.user_data.get("awaiting_phone"):
#         user = session.query(CustomUser).filter_by(phone=phone).first()
#         if user:
#             user.telegram_id = telegram_id
#             session.commit()
#             await update.message.reply_text("Вы успешно зарегистрированы в системе!")
#         else:
#             await update.message.reply_text("Пользователь с таким номером не найден.")
#         context.user_data["awaiting_phone"] = False
#         session.close()
#
# def main():
#     app = ApplicationBuilder().token(BOT_TOKEN).build()
#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
#     app.run_polling()
#
# if __name__ == "__main__":
#     main()
