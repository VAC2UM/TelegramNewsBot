import requests
from bs4 import BeautifulSoup
import codecs
import time


def KinoAfisha_parser(back_post_title):
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
        return None

def Letterboxd_parser():
    URL = "https://letterboxd.com/vac2um/films/diary/"
    response = requests.get(URL)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        link = soup.find('h3', class_='headline-3 prettify').a.get('href')

        page2 = requests.get("https://letterboxd.com" + link)
        soup2 = BeautifulSoup(page2.content, "html.parser")

        review = soup2.findAll('div', class_='review body-text -prose -hero -loose')
        print(review)
    else:
        print(f"Failed to retrieve the webpage, status code: {response.status_code}")


# реализовать изменение title в txt файле при несовпадении
# while True:
#     with open('../main/last_title.txt', encoding='utf-8', mode='r', errors='ignore') as back_post_title:
#         last_title = back_post_title.read()
#
#         URL = "https://www.kinoafisha.info/news/"
#         page = requests.get(URL)
#         soup = BeautifulSoup(page.content, "html.parser")
#
#         post = soup.find('span', class_='newsV2_title').get_text(strip=True)
#
#         while True:
#             if post != last_title:
#                 # бот выводит новый пост
#                 print(KinoAfisha_parser(last_title))
#
#                 with codecs.open('../main/last_title.txt', 'w', 'utf-8', errors='ignore') as f:
#                     f.write(post)
#                     f.close()
#                 break
#             else:
#                 break
#         back_post_title.close()
#     time.sleep(1800)


Letterboxd_parser()