import telebot
from dotenv import load_dotenv
from os import environ
import time
from parsers import Parsers

load_dotenv()

token = environ.get('TOKEN')
id_channel = environ.get('ID_CHANNEL')
bot = telebot.TeleBot(token)
URL_KinoAfisha = "https://www.kinoafisha.info/news/"
URL_diary = "https://letterboxd.com/vac2um/films/diary/"

if __name__ == '__main__':
    my_parser = Parsers(bot, id_channel, URL_KinoAfisha, URL_diary)
    my_parser.commands()