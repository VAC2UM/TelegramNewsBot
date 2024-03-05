import telebot
from dotenv import load_dotenv
from os import environ

import requests
from bs4 import BeautifulSoup

load_dotenv()

token = environ.get('TOKEN')
id_channel = environ.get('ID_CHANNEL')
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=["text"])
def commands(message):
    bot.send_message(id_channel, message.text)

# def parser():

# bot.polling()