import os
import sys
import logging
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bot.models import CustomUser

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")


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

