from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

import os

TOKEN = os.environ.get("TOKEN")


# ---------- ФАЙЛЫ ----------

FILES = {
    "complaints": "complaints.txt",
    "news": "news.txt",
    "photos": "photos.txt"
}

# Создаём файлы, если их нет
for f in FILES.values():
    if not os.path.exists(f):
        with open(f, "w", encoding="utf-8") as file:
            pass

# ---------- КНОПКИ ----------

def main_menu():
    return ReplyKeyboardMarkup(
        [
            ["📰 Новости", "📸 Фото"],
            ["📝 Жалобы", "📞 Контакты"]
        ],
        resize_keyboard=True
    )

def news_menu():
    return ReplyKeyboardMarkup(
        [
            ["📢 Последние новости", "📅 Архив новостей"],
            ["➕ Добавить новость", "🔙 Назад"]
        ],
        resize_keyboard=True
    )

def photos_menu():
    return ReplyKeyboardMarkup(
        [
            ["📷 Новые фото", "🏞️ Архив фото"],
            ["➕ Добавить фото", "🔙 Назад"]
        ],
        resize_keyboard=True
    )

def complaints_menu():
    return ReplyKeyboardMarkup(
        [
            ["⚠️ Добавить жалобу", "📄 Просмотреть жалобы"],
            ["🔙 Назад"]
        ],
        resize_keyboard=True
    )

# ---------- СТАТУС ПОЛЬЗОВАТЕЛЯ ----------

user_waiting_for = {}  # user_id: "complaint"/"news"/"photo"

# ---------- КОМАНДЫ ----------

def start(update, context):
    update.message.reply_text(
        "Привет! Добро пожаловать в семейный бот ❤️\nВыбери раздел:",
        reply_markup=main_menu()
    )

def handle_message(update, context):
    user_id = update.message.from_user.id
    text = update.message.text

    # Проверка, ждём ли текст для добавления
    if user_id in user_waiting_for:
        action = user_waiting_for[user_id]

        if action == "complaint":
            with open(FILES["complaints"], "a", encoding="utf-8") as f:
                f.write(text + "\n")
            update.message.reply_text("✅ Жалоба сохранена!", reply_markup=main_menu())

        elif action == "news":
            with open(FILES["news"], "a", encoding="utf-8") as f:
                f.write(text + "\n")
            update.message.reply_text("✅ Новость добавлена!", reply_markup=main_menu())

        elif action == "photo":
            with open(FILES["photos"], "a", encoding="utf-8") as f:
                f.write(text + "\n")
            update.message.reply_text("✅ Фото добавлено!", reply_markup=main_menu())

        # Убираем статус ожидания
        del user_waiting_for[user_id]
        return

    # Главное меню
    if text == "📰 Новости":
        update.message.reply_text("Новости:", reply_markup=news_menu())

    elif text == "📸 Фото":
        update.message.reply_text("Фото семьи:", reply_markup=photos_menu())

    elif text == "📝 Жалобы":
        update.message.reply_text("Жалобы и предложения:", reply_markup=complaints_menu())

    elif text == "📞 Контакты":
        update.message.reply_text("Контакты семьи 📱")

    # ---------- Новости ----------
    elif text == "📢 Последние новости":
        with open(FILES["news"], "r", encoding="utf-8") as f:
            data = f.read().strip()
        if data:
            update.message.reply_text(f"📋 Новости:\n{data}")
        else:
            update.message.reply_text("Пока нет новостей 📰")

    elif text == "📅 Архив новостей":
        with open(FILES["news"], "r", encoding="utf-8") as f:
            data = f.read().strip()
        if data:
            update.message.reply_text(f"🗂️ Архив новостей:\n{data}")
        else:
            update.message.reply_text("Архив пуст 🗂️")

    elif text == "➕ Добавить новость":
        update.message.reply_text("Отправьте текст новости 📰")
        user_waiting_for[user_id] = "news"

    # ---------- Фото ----------
    elif text == "📷 Новые фото":
        with open(FILES["photos"], "r", encoding="utf-8") as f:
            data = f.read().strip()
        if data:
            update.message.reply_text(f"📸 Новые фото:\n{data}")
        else:
            update.message.reply_text("Пока нет фото 📸")

    elif text == "🏞️ Архив фото":
        with open(FILES["photos"], "r", encoding="utf-8") as f:
            data = f.read().strip()
        if data:
            update.message.reply_text(f"🗂️ Архив фото:\n{data}")
        else:
            update.message.reply_text("Архив фото пуст 🗂️")

    elif text == "➕ Добавить фото":
        update.message.reply_text("Отправьте ссылку или название фото 📷")
        user_waiting_for[user_id] = "photo"

    # ---------- Жалобы ----------
    elif text == "⚠️ Добавить жалобу":
        update.message.reply_text("Отправьте текст вашей жалобы 📝")
        user_waiting_for[user_id] = "complaint"

    elif text == "📄 Просмотреть жалобы":
        with open(FILES["complaints"], "r", encoding="utf-8") as f:
            data = f.read().strip()
        if data:
            update.message.reply_text(f"📋 Все жалобы:\n{data}")
        else:
            update.message.reply_text("Пока нет жалоб 📝")

    # ---------- Назад ----------
    elif text == "🔙 Назад":
        update.message.reply_text("Главное меню:", reply_markup=main_menu())

    else:
        update.message.reply_text("Пожалуйста, выбери кнопку 👇")

# ---------- ЗАПУСК ----------

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    print("✅ Бот запущен. Ctrl+C чтобы остановить.")
    updater.idle()

if __name__ == "__main__":
    main()

