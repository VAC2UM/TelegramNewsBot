import requests
from bs4 import BeautifulSoup
import codecs
import pyshorteners
import re
from deep_translator import GoogleTranslator

URL_diary = "https://letterboxd.com/vac2um/films/diary/"


def shorten_url(url):
    return pyshorteners.Shortener().clckru.short(url)

def translate_text(text, dest_lang='ru'):
    return GoogleTranslator(source='auto', target=dest_lang).translate(text)


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

        link = format(shorten_url(link))
        return f"{title}\n\n{description}\n{'#новости'}\n\n{link}"
    else:
        return None


def Letterboxd_parser(back_review):
    URL_my_page = "https://letterboxd.com/Vac2um/"

    response = requests.get(URL_diary)
    response_my_page = requests.get(URL_my_page)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        soup_my_page = BeautifulSoup(response_my_page.text, "html.parser")

        link = soup.find('h3', class_='headline-3 prettify').a.get('href')
        review_link = "https://letterboxd.com" + link
        review_link = format(shorten_url(review_link))

        page2 = requests.get("https://letterboxd.com" + link)
        soup2 = BeautifulSoup(page2.content, "html.parser")

        review = soup2.find('div', class_='review').get_text(strip=True)
        filmLink = soup2.find('span', class_='film-title-wrapper').a.get('href')

        film_page = requests.get("https://letterboxd.com" + filmLink)
        film_page_soup = BeautifulSoup(film_page.content, "html.parser")

        description = film_page_soup.find('div', class_='truncate').text.strip()
        description = translate_text(description)

        title_tag = soup2.find('span', class_='film-title-wrapper').a
        title_text = title_tag.text.strip()

        author = "V A C U U M’s review published on Letterboxd:"

        mark = soup_my_page.find('p', class_='poster-viewingdata').get_text().strip()

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

        review = review.replace(author, "")
        review = re.sub(r'\.(?=[^\s])', '.\n', review)

        noReview = "There is no review for this diary entry"

        diaryURL = "https://letterboxd.com/vac2um/films/diary/"
        diaryResponse = requests.get(diaryURL)
        diarySoup = BeautifulSoup(diaryResponse.text, "html.parser")
        year_tag = diarySoup.find('td', class_='td-released center')
        year_text = year_tag.text.strip()

        # Если отзыва нет
        if noReview in review:
            return f"{title_text + ' '}{year_text}\n\n{description}\n\n{review_link}\n\n{'#оценка'}\n{'Моя оценка: '}{switch.get(mark)}{'/10'}"

        return f"{title_text + ' '}{year_text}\n\n{description}\n\n{'#отзыв'}\n{review}\n{review_link}\n\n{'#оценка'}\n{'Моя оценка: '}{switch.get(mark)}{'/10'}"
    else:
        print(f"Failed to retrieve the webpage, status code: {response.status_code}")


# реализовать изменение title в txt файле при несовпадении
while True:
    with open('../main/last_title.txt', encoding='utf-8', mode='r', errors='ignore') as back_post_title:
        last_title = back_post_title.read()

        URL = "https://www.kinoafisha.info/news/"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        post = soup.find('span', class_='newsV2_title').get_text(strip=True)

        while True:
            if post != last_title:
                # бот выводит новый пост
                print(KinoAfisha_parser(last_title))

                with codecs.open('../main/last_title.txt', 'w', 'utf-8', errors='ignore') as f:
                    f.write(post)
                    f.close()
                break
            else:
                break
        back_post_title.close()
    with open('../main/last_review.txt', encoding='utf-8', mode='r', errors='ignore') as back_review_title:
        last_review = back_review_title.read()

        page = requests.get(URL_diary)
        soup = BeautifulSoup(page.content, "html.parser")

        review = soup.find('h3', class_='headline-3 prettify').a
        review_text = review.text.strip()

        if review_text != last_review:
            print(Letterboxd_parser(last_review))

            with codecs.open('../main/last_review.txt', 'w', 'utf-8', errors='ignore') as f:
                f.write(review_text)
                f.close()
            break
        else:
            print("Review has not updated")
            break
    time.sleep(1800)
