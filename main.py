from pprint import pprint
import telebot
import requests
from config import TELEGRAM_TOKEN, API_URL

bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message, "Howdy, Give me a keyword for me to search latest news for you")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(
        message.chat.id, "<b>Searching for News...</b>", parse_mode="HTML")
    url = API_URL + "news/search/" + message.text
    response = requests.request("GET", url)

    result = response.json()
    for r in result:

        bot_message = "<a href='"+r['link']+"'><b>"+r['title']+"</b></a>"
        bot.send_message(message.chat.id, bot_message,
                         parse_mode="HTML")


bot.infinity_polling()
