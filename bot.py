from config import TOKEN
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from logic import *
bot = TeleBot(TOKEN)
def gen_markup(id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Да", callback_data=id))
    return markup
def gea_markup(id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Нет", callback_data=id))
    return markup

from logic import DB_Manager
from config import *
from telebot import TeleBot

bot = TeleBot(TOKEN)





@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! \nДоступные команды:\n"
                         "/add <название> — добавить канал в избранное\n"
                         "/show — показать твои избранные каналы\n"
                         "/delete - удалить из избранных\n"
                         "/find - найти канал")

@bot.message_handler(commands=["add"])
def add(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, "Укажи название канала. Пример:\n`/add TechNews`", parse_mode="Markdown")
        return
    name = parts[1]
    result = manager.add_favorite(name)
    bot.reply_to(message, result)

@bot.message_handler(commands=['show'])
def show_favorites(message):
    favorites = manager.my_favorites()
    if not favorites:
        bot.reply_to(message, "У тебя пока нет избранных каналов.")
        return

    text = "\n".join(f"• {channel}" for channel in favorites)
    bot.reply_to(message, f"Твои избранные каналы:\n{text}")

@bot.message_handler(commands=["delete"])
def delete(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        favorites = manager.my_favorites()
        if not favorites:
            bot.reply_to(message, "У тебя пока нет избранных каналов.")
            return

        text = "\n".join(f"• {channel}" for channel in favorites)
        bot.reply_to(message, f"Твои избранные каналы:\n{text}\nКакого стримера удалить. \n Напиши /delete и название канала")
    else:
        name = parts[1]
        result = manager.delete(name)
        bot.reply_to(message, result)

@bot.message_handler(commands=["find"])
def find(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.send_message(message.chat.id, "Ты не написал название канала")
    else:
        names = parts[1]
        result = manager.find_acc(names)
        bot.reply_to(message, "\n".join(result) if result else "Ничего не найдено")

@bot.message_handler(commands=["info"])
def info(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.send_message(message.chat.id, "Ты не написал название канала")
    else:
        names = parts[1]
        result = manager.infok(names)
        if len(result) > 1:
            bot.send_message(message.chat.id, "Было найдено много каналов с похожем именем, которое вы отправили")
            result = manager.find_acc(names)
            bot.reply_to(message, "\n".join(result))
            bot.send_message(message.chat.id, "Кто иммено из них")

@bot.callback_query_handler(func=lambda call: True)
def talk(message):
    bot.send_message(message.chat.id, "Привет!" )
    

if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    bot.infinity_polling()