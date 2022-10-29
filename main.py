import requests
from bs4 import BeautifulSoup
from config import *
import json
import re
from time import time


r = requests.get(url=url, headers=headers, proxies=proxies)
soup = BeautifulSoup(r.text, "lxml")

# with open("data/index.html", encoding='utf8') as fp:
#     soup = BeautifulSoup(fp, "lxml")

def get_news():

    articles_cards = soup.find_all("article", class_='tm-articles-list__item')
    # articles_cards_desc = soup.find_all("div", class_='article-formatted-body article-formatted-body article-formatted-body_version-2')

    new_dict = {}
    for article in articles_cards:

        article_url = article.find("h2").find("a").get("href")
        article_id = article_url.split("/")[-2]
        article_id = article_url.split("/")[-2]

        # url_habr_json = f'https://habr.com/kek/v2/articles/{article_id}/similar?fl=ru&hl=ru'
        url_habr_json = f'https://habr.com/kek/v2/articles/{article_id}/?fl=ru&hl=ru'
        r = requests.get(url=url_habr_json, headers=headers, proxies=proxies)

        with open("s.json", "w", encoding="utf8") as file:
            json.dump(r.json(), file, indent=4, ensure_ascii=False)

        with open("s.json", encoding='utf8') as file:
            news_dict = json.load(file)

        articles_title = news_dict["titleHtml"]
        articles_id = news_dict["id"]
        articles_desc = news_dict["leadData"]["textHtml"]
        articles_time = news_dict["timePublished"]
        articles_author = news_dict["author"]["alias"]
        articles_Plus = news_dict["statistics"]["votesCountPlus"]
        articles_Minus = news_dict["statistics"]["votesCountMinus"]
        article_corporation = news_dict["isCorporative"]

        if (article_corporation == True):
            article_url = f'https://habr.com/ru/company/cloud4y/blog/{articles_id}/'
        else:
            article_url = f'https://habr.com/ru/post/{articles_id}/'

        new_dict[article_id] = {
            "articles_title": articles_title,
            "articles_id": articles_id,
            "articles_time": articles_time,
            "articles_author": articles_author,
            "articles_Plus": articles_Plus,
            "articles_Minus": articles_Minus,
            "articles_corporation": article_corporation,
            "articles_url": article_url
        }


        with open("news_dict.json", "w", encoding="utf8") as file:
            json.dump(new_dict, file, indent=4, ensure_ascii=False)



def check_news_update():
    with open("news_dict.json", encoding='utf8') as file:
        news_dict = json.load(file)

    articles_cards = soup.find_all("article", class_='tm-articles-list__item')


    fresh_news = {}
    for article in articles_cards:
        article_url_pre = article.find("h2")
        article_url_pre_2 = article_url_pre.find("a")
        article_url = f'{article_url_pre_2.get("href")}'
        article_id = article_url.split("/")[-1]
        article_id = article_id[:-4]

        try:
            if article_id in news_dict:
                continue
            else:
                article_title = article.find("h2").text
                article_desc_pre = article.find("div")
                article_desc = article_desc_pre.find("p").text
                article_url_pre = article.find("h2")
                article_url_pre_2 = article_url_pre.find("a")
                article_url = f'{article_url_pre_2.get("href")}'

                article_id = article_url.split("/")[-2]

        except AttributeError:
            pass

            news_dict[article_id] = {
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }

            fresh_news[article_id] = {
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }

    with open("news_dict.json", "w", encoding="utf8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


def main():
    get_news()
    print(check_news_update())

if __name__ == '__main__':
    main()

