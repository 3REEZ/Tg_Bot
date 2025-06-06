from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import feedparser

# Настройки
TOKEN = "7907172759:AAHpLLq0vbMdjAizweCBS-S1ZoQ3PHjK-HA"
CHANNEL_ID = "@IT32SQUAD"  # или ID чата (например, -100123456789)

# Функция для получения новостей
async def get_tech_news():
    feed = feedparser.parse("https://techcrunch.com/feed/")
    return [f"📢 {entry.title}\n\n{entry.link}" for entry in feed.entries[:5]]

# Обработчик команды /news
async def send_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news = await get_tech_news()
    for item in news:
        await context.bot.send_message(chat_id=CHANNEL_ID, text=item)

# Запуск бота
def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("news", send_news))
    application.run_polling()

if __name__ == "__main__":
    from apscheduler.schedulers.background import BackgroundScheduler


    def auto_post():
        for item in get_tech_news():
            updater.bot.send_message(chat_id=CHANNEL_ID, text=item)


    scheduler = BackgroundScheduler()
    scheduler.add_job(auto_post, 'interval', hours=2)  # каждые 2 часа
    scheduler.start()
    main()