from config import *
import requests
import json
from bs4 import BeautifulSoup

url = 'https://habr.com/ru/flows/develop/'
r = requests.get(url=url, headers=headers, proxies=proxies)

new_dict = {}
def get_dev_news():

    url = 'https://habr.com/ru/flows/develop/'
    r = requests.get(url=url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(r.text, "lxml")

    article_card = soup.find_all("article", class_='tm-articles-list__item')

    for article in article_card:
        article_url = article.find("h2").find("a").get("href")
        article_id = article_url.split("/")[-2]
        article_id = article_url.split("/")[-2]

        url_dev_json = f'https://habr.com/kek/v2/articles/{article_id}/?fl=ru&hl=ru'
        r_dev = requests.get(url=url_dev_json, headers=headers, proxies=proxies)

        with open("json/dev.json", "w", encoding="utf8") as file:
            json.dump(r_dev.json(), file, indent=4, ensure_ascii=False)

        with open("json/dev.json", encoding="utf8") as file:
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

        with open("json/dev_ready.json", "w", encoding="utf8") as file:
            json.dump(new_dict, file, indent=4, ensure_ascii=False)

def check_news_update():
    with open("json/dev_ready.json", encoding="utf8") as file:
        news_dict = json.load(file)

    url = 'https://habr.com/ru/flows/develop/'
    r = requests.get(url=url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(r.text, "lxml")

    article_card = soup.find_all("article", class_='tm-articles-list__item')

    fresh_news = {}
    for article in article_card:
        article_url = article.find("h2").find("a").get("href")
        article_id = article_url.split("/")[-2]
        article_id = article_url.split("/")[-2]

        url_dev_json = f'https://habr.com/kek/v2/articles/{article_id}/?fl=ru&hl=ru'
        r_dev = requests.get(url=url_dev_json, headers=headers, proxies=proxies)

        with open("json/dev.json", "w", encoding="utf8") as file:
            json.dump(r_dev.json(), file, indent=4, ensure_ascii=False)

        with open("json/dev.json", encoding="utf8") as file:
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

        fresh_news[article_id] = {
            "articles_title": articles_title,
            "articles_id": articles_id,
            "articles_time": articles_time,
            "articles_author": articles_author,
            "articles_Plus": articles_Plus,
            "articles_Minus": articles_Minus,
            "articles_corporation": article_corporation,
            "articles_url": article_url
        }

        with open("json/dev_ready.json", "w", encoding="utf8") as file:
            json.dump(new_dict, file, indent=4, ensure_ascii=False)

    return fresh_news

def main():
    get_dev_news()
    print(check_news_update())

if __name__ == "__main__":
    main()