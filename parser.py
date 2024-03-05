import requests
from bs4 import BeautifulSoup
import urllib.request

#
# URL = "https://www.kinoafisha.info/news/"
#
# page = requests.get(URL)
# soup = BeautifulSoup(page.content, "html.parser")
#
# post = soup.find("a", class_="newsV2_top")
#
# title = post.find("span", class_="newsV2_title").text.strip()
# description = post.find("span", class_="newsV2_desc").text.strip()
# # url = post.find("span", class_="newsV2_title", href=True)["href"].strip()

URL = "https://www.kinoafisha.info/news/"

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

# link to film description
link = soup.find('div', class_='newsV2_item').a.get('href')

page2 = requests.get(link)
soup2 = BeautifulSoup(page2.content, "html.parser")

post = soup2.find("div", class_="article_column")
post_description = soup2.find("div", class_="article_content visualEditorInsertion visualEditorInsertion-large")

title = post.find("h1", class_="article_title").text.strip()
description = post_description.find("p").text.strip()
print(title + "\n")
print(description)
print(link)
