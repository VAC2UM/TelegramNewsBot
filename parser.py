import requests
from bs4 import BeautifulSoup
import  codecs

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
        return None


# реализовать изменение title в txt файле при несовпадении
with open('last_title.txt', encoding='utf-16', mode='r') as back_post_title:
    last_title = back_post_title.read()

    URL = "https://www.kinoafisha.info/news/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    post = soup.find('span', class_='newsV2_title').text.strip()

    while True:
        if post != last_title:
            # бот выводит новый пост
            print(parser(last_title))

            with codecs.open('last_title.txt', 'w', 'utf-16') as f:
                f.write(post)
                f.close()
            break
        else:
            break
    back_post_title.close()