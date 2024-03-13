import telebot

from dotenv import load_dotenv
from os import environ

import requests
from bs4 import BeautifulSoup
import time
import codecs

import re

load_dotenv()

token = environ.get('TOKEN')
id_channel = environ.get('ID_CHANNEL')
bot = telebot.TeleBot(token)

URL_diary = "https://letterboxd.com/vac2um/films/diary/"

# @bot.message_handler(content_types=["text"])
def commands():
    while True:
        with open('last_title.txt', encoding='utf-8', mode='r', errors='ignore') as back_post_title:
            last_title = back_post_title.read()

            URL = "https://www.kinoafisha.info/news/"
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")

            post = soup.find('span', class_='newsV2_title').get_text(strip=True)

            while True:
                if post != last_title:
                    # бот выводит новый пост
                    bot.send_message(id_channel, parser(last_title))

                    with codecs.open('last_title.txt', 'w', 'utf-8', errors='ignore') as f:
                        f.write(post)
                        f.close()
                    break
                else:
                    break
            back_post_title.close()
        with open('last_review.txt', encoding='utf-8', mode='r', errors='ignore') as back_review_title:
            last_review = back_review_title.read()

            page = requests.get(URL_diary)
            soup = BeautifulSoup(page.content, "html.parser")

            review = soup.find('h3', class_='headline-3 prettify').a
            review_text = review.text.strip()

            if review_text != last_review:
                bot.send_message(id_channel, Letterboxd_parser(last_review))

                with codecs.open('last_review.txt', 'w', 'utf-8', errors='ignore') as f:
                    f.write(review_text)
                    f.close()
                break
            else:
                print("Review has not updated")
                break
        time.sleep(1800)
    # while True:
    #     with open('last_title.txt', encoding='utf-8', mode='r', errors='ignore') as back_post_title:
    #         last_title = back_post_title.read()
    #
    #         URL = "https://www.kinoafisha.info/news/"
    #         page = requests.get(URL)
    #         soup = BeautifulSoup(page.content, "html.parser")
    #         post = soup.find('span', class_='newsV2_title').text.strip()
    #
    #         if post != last_title:
    #             # bot print new post
    #             bot.send_message(id_channel, parser(last_title))
    #
    #             with codecs.open('last_title.txt', 'w', 'utf-8', errors='ignore') as f:
    #                 f.write(post)
    #                 f.close()
    #         else:
    #             print("Post has not updated")
    #         back_post_title.close()
    #     time.sleep(1800)


def parser(back_post_title):
    URL = "https://www.kinoafisha.info/news/"

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    post = soup.find('span', class_='newsV2_title').text.strip()

    if post != back_post_title:
        # link to film description
        link = soup.find('div', class_='newsV2_item').a.get('href')

        page2 = requests.get(link)
        soup2 = BeautifulSoup(page2.content, "html.parser")

        second_post = soup2.find("div", class_="article_column")
        post_description = soup2.find("div", class_="article_content visualEditorInsertion visualEditorInsertion-large")

        title = second_post.find("h1", class_="article_title").text.strip()
        description = post_description.find("p").text.strip()

        return f"{title}\n\n{description}\n\n{link}"
    else:
        return None, post


def Letterboxd_parser(back_review):
    URL_my_page = "https://letterboxd.com/Vac2um/"

    response = requests.get(URL_diary)
    response_my_page = requests.get(URL_my_page)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        soup_my_page = BeautifulSoup(response_my_page.text, "html.parser")

        link = soup.find('h3', class_='headline-3 prettify').a.get('href')

        page2 = requests.get("https://letterboxd.com" + link)
        soup2 = BeautifulSoup(page2.content, "html.parser")

        review = soup2.find('div', class_='review').get_text(strip=True)

        title_tag = soup2.find('span', class_='film-title-wrapper').a
        title_text = title_tag.text.strip()
        # title_link = title_tag['href']

        year_tag = soup2.find('small', class_='metadata').a
        year_text = year_tag.text.strip()

        author = "V A C U U M’s review published on Letterboxd:"

        mark = soup_my_page.find('span',class_='rating rated-8').get_text().strip()
        switch = {
            "★★★★★": 10,
            "★★★★½": 9,
            "★★★★": 8,
            "★★★½": 7,
            "★★★": 6,
            "★★½": 5,
            "★★": 4,
            "★½": 3,
            "★": 2,
            "½": 1,
        }

        review = review.replace(author,"")
        review = re.sub(r'\.(?=[^\s])', '.\n', review)

        return f"{title_text + ' '}{year_text}\n\n{review}\n\n{'Моя оценка: '}{switch.get(mark)}{'/10'}"
    else:
        print(f"Failed to retrieve the webpage, status code: {response.status_code}")

if __name__ == '__main__':
    bot.polling(commands())
