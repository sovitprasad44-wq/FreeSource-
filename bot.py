import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Token Render / Hosting ke Environment Variable se aayega
TOKEN = os.getenv("8595448022:AAEudm9ozX0PM60YjZDCkSZRkEa8mI29l8k")

bot = telebot.TeleBot(TOKEN)

CHANNEL = "@ai_science_official"
GROUP = "@ai_science_group"

def is_joined(user_id):
    try:
        ch = bot.get_chat_member(CHANNEL, user_id)
        gr = bot.get_chat_member(GROUP, user_id)
        return ch.status in ['member', 'administrator', 'creator'] and \
               gr.status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    if is_joined(message.from_user.id):
        bot.send_message(
            message.chat.id,
            "✅ Access Granted!\nWelcome to AI Science Bot 🚀"
        )
    else:
        kb = InlineKeyboardMarkup()
        kb.add(
            InlineKeyboardButton("🔔 Join Channel", url="https://t.me/ai_science_official"),
            InlineKeyboardButton("👥 Join Group", url="https://t.me/ai_science_group")
        )
        kb.add(
            InlineKeyboardButton("✅ I Joined", callback_data="check")
        )
        bot.send_message(
            message.chat.id,
            "❌ Pehle dono join karo, tabhi bot use hoga 👇",
            reply_markup=kb
        )

@bot.callback_query_handler(func=lambda call: call.data == "check")
def check_join(call):
    if is_joined(call.from_user.id):
        bot.edit_message_text(
            "✅ Access Granted!\nWelcome to AI Science Bot 🚀",
            call.message.chat.id,
            call.message.message_id
        )
    else:
        bot.answer_callback_query(
            call.id,
            "❌ Abhi join nahi kiya hai",
            show_alert=True
        )

bot.infinity_polling()