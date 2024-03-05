import requests
from bs4 import BeautifulSoup


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


# main
with open('last_title.txt', encoding='utf-8', mode='r') as back_post_title:
    last_title = back_post_title.read()
    parser(last_title)
    # реализовать изменение title в txt файле при несовпадении

    # print(last_title)
    # print(parser(last_title))



# back_post_title = ""
# while True:
#     post_text = parser(back_post_title)
#     back_post_title = post_text[1]
#
#     if post_text[0] != None:
#         print(post_text[0])


# print(title + "\n")
# print(description)
# print(link)
