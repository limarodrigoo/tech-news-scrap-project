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


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
