from time import sleep
from parsel import Selector
import requests

from tech_news.database import create_news


# Requisito 1
def fetch(url):
    try:
        sleep(1)
        res = requests.get(
            url, headers={"user-agent": "Fake user-agent"}, timeout=3
        )
    except requests.ReadTimeout:
        res = None
    finally:
        if res is None:
            return None
        elif res.status_code == 200:
            return res.text
        else:
            return None


# Requisito 2
def scrape_novidades(html_content):
    selector = Selector(text=html_content)
    links = selector.css(
        ".cs-container .post .post-inner .cs-overlay-link::attr(href)"
    ).getall()
    return links


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    next_page_link = selector.css(".next::attr(href)").get()
    return next_page_link


# Requisito 4
def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    url = selector.css("link[rel=canonical]::attr(href)").get()
    title = selector.css("h1.entry-title::text").get()
    author = selector.css(".author a::text").get()
    date = selector.css(".meta-date::text").get()
    comments = len(selector.css(".comment-body").getall())
    summary = selector.css(
        "div.entry-content > p:nth-of-type(1) *::text"
    ).getall()
    category = selector.css("div.meta-category span.label::text").get()
    tags = selector.css("section.post-tags li a::text").getall()
    title = title.strip()
    summary = "".join(summary).strip()
    return {
        "url": url,
        "title": title,
        "timestamp": date,
        "writer": author,
        "comments_count": comments,
        "summary": summary,
        "tags": tags,
        "category": category,
    }


def get_tech_news_helper(news_link_list, amount):
    news_list = []
    length_links_list = len(news_link_list)
    qty_needed = length_links_list - (length_links_list % amount)
    news_link_list = news_link_list[:qty_needed]
    for news_link in news_link_list:
        news_html = fetch(news_link)
        news_data = scrape_noticia(news_html)
        news_list.append(news_data)
    return news_list


# Requisito 5
def get_tech_news(amount):
    news_list = []
    url = "https://blog.betrybe.com"
    while len(news_list) < amount:
        html_content = fetch(url)
        news_link_list = scrape_novidades(html_content)
        # set quantity of news needed in the next request package
        next_package_needed = len(news_link_list)
        # if the amount needed is lower then the number of the default
        # package length
        if (amount - len(news_list)) < len(news_link_list):
            # amount from the beginning is alread lower then the package
            if amount < len(news_link_list):
                next_package_needed = amount
            # quantity needed is higher then the default package length
            else:
                next_package_needed = amount - len(news_list)
        news_list += get_tech_news_helper(news_link_list, next_package_needed)
        url = scrape_next_page_link(html_content)
    create_news(news_list)
