import telebot
from telebot.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
import json

# @BotFather'dan math1010_bot uchun olgan tokeningizni yozing
TOKEN = "SIZNING_BOT_TOKENINGIZ"
bot = telebot.TeleBot(TOKEN)

# GitHub Pages'dan olingan index.html havolasini yozing
WEB_APP_URL = "https://username.github.io/repo-nomi/index.html"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    web_app = WebAppInfo(url=WEB_APP_URL)
    markup.add(InlineKeyboardButton("🧠 Matematika darajasini aniqlash", web_app=web_app))
    
    bot.send_message(
        message.chat.id, 
        "Salom! Ushbu mini ilova yordamida matematika bilim darajangizni 10 xil turdagi savollar orqali sinovdan o'tkazing.",
        reply_markup=markup
    )

@bot.message_handler(content_types=['web_app_data'])
def receive_webapp_data(message):
    data = json.loads(message.web_app_data.data)
    score = data.get('score', 0)
    bot.send_message(message.chat.id, f"Test yakunlandi! Sizning umumiy ballingiz: {score} / 10 🎯")

if __name__ == '__main__':
    print("Bot ishga tushdi...")
    bot.infinity_polling()
