from datetime import datetime
from tech_news.database import search_news


def tuple_builder(cursor):
    news_list = []
    for news in cursor:
        news_list.append((news["title"], news["url"]))

    return news_list


# Requisito 6
def search_by_title(title):
    cursor = search_news({"title": {"$regex": title, "$options": "i"}})

    return tuple_builder(cursor)


# Requisito 7
def search_by_date(date):
    try:
        date = datetime.fromisoformat(date).strftime("%d/%m/%Y")
        cursor = search_news({"timestamp": date})
        return tuple_builder(cursor)

    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_tag(tag):
    cursor = search_news(
        {"tags": {"$elemMatch": {"$regex": tag, "$options": "i"}}}
    )
    return tuple_builder(cursor)


# Requisito 9
def search_by_category(category):
    cursor = search_news({"category": {"$regex": category, "$options": "i"}})
    return tuple_builder(cursor)
