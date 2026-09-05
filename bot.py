import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from telebot.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
import json

# Tokeningizni yozing
TOKEN = "8978768448:AAEhkeTQMTktCnq8K6yWAQIBtw1QQ1zp8YY
"
bot = telebot.TeleBot(TOKEN)

# GitHub Pages havolangiz
WEB_APP_URL = "https://dilshodbekbegmamatov25-hue.github.io/math1010_bot/"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    web_app = WebAppInfo(url=WEB_APP_URL)
    markup.add(InlineKeyboardButton("🧠 Matematika darajasini aniqlash", web_app=web_app))
    
    bot.send_message(
        message.chat.id, 
        "Salom! Testni boshlash uchun quyidagi tugmani bosing:",
        reply_markup=markup
    )

# Render port talabini qondirish va natijani qabul qilish uchun server
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

    def do_POST(self):
        if self.path == '/submit':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                user_id = data.get('user_id')
                name = data.get('name')
                score = data.get('score')
                
                if user_id:
                    level_text = "Boshlang'ich"
                    if score > 7:
                        level_text = "Yuqori / Professional! 🏆"
                    elif score > 4:
                        level_text = "O'rta"

                    bot.send_message(
                        user_id, 
                        f"🎉 **Test yakunlandi!**\n\n"
                        f"📊 Sizning natijangiz: 10 ta savoldan {score} ta to'g'ri\n"
                        f"💡 Darajangiz: 🥉 {level_text}", 
                        parse_mode="Markdown"
                    )
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"Success")
                    return
            except Exception as e:
                print("Xatolik:", e)
        
        self.send_response(400)
        self.end_headers()
        self.wfile.write(b"Bad Request")

def run_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

if __name__ == '__main__':
    threading.Thread(target=run_web, daemon=True).start()
    print("Bot va veb-server ishga tushdi...")
    bot.infinity_polling()
