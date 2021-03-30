import typing as tp

import requests
from bs4 import BeautifulSoup


def extract_news(parser: BeautifulSoup) -> tp.List[tp.Dict[str, tp.Union[int, str]]]:
    """ Extract news from a given web page """
    news_list = []
    storylinks = parser.select(".storylink")
    users = parser.select(".hnuser")
    scores = parser.select(".score")

    index = 0
    for storylink in storylinks:
        link = storylink["href"]
        title = storylink.get_text()
        author = users[index].get_text()
        score = int(scores[index].get_text().split(" ")[0])
        if link.startswith("item"):
            link = "https://news.ycombinator.com/newest" + link
        news_list.append({"author": author, "points": score, "title": title, "url": link})
        index += 1

    return news_list


def extract_next_page(parser: BeautifulSoup) -> str:
    """ Extract next page URL """
    return str(parser.select(".morelink")[0]["href"])


def get_news(url: str, n_pages: int = 1) -> tp.List[tp.Dict[str, tp.Union[int, str]]]:
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news


if __name__ == "__main__":
    news = get_news("https://news.ycombinator.com/newest", 3)
