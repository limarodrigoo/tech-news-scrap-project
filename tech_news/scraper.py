from time import sleep
from parsel import Selector
import requests


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
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
