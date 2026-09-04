import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from telebot.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
import json

# BotFather'dan olingan math1010_bot tokeningizni yozing
TOKEN = "8978768448:AAEhkeTQMTktCnq8K6yWAQIBtw1QQ1zp8YY"
bot = telebot.TeleBot(TOKEN)

# GitHub Pages'dan olingan index.html havolasini yozing
WEB_APP_URL = "https://dilshodbekbegmamatov25-hue.github.io/math1010_bot/"

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

# --- Render port talabini qondirish uchun kichik veb-server ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

if __name__ == '__main__':
    # Veb-serverni alohida oqimda (thread) ishga tushiramiz
    threading.Thread(target=run_web, daemon=True).start()
    
    print("Bot va veb-server ishga tushdi...")
    bot.infinity_polling()
