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
    bot.delete_message(message.chat.id, "")
    bot.send_message(message.chat.id, "Searching for News...")
    url = API_URL + "news/search/" + message.text
    response = requests.request("GET", url)

    result = response.json()
    for r in result:

        bot_message = "<b>"+r['title']+"</b> \n<i>From: "+r['src']+" \nTime: " + \
            r['time']+" </i> \n<a href='"+r['link']+"'><b>Read Now!</b></a>"
        bot.send_message(message.chat.id, bot_message,
                         parse_mode="HTML", disable_web_page_preview=True)


bot.infinity_polling()
