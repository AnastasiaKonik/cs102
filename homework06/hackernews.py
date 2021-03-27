import typing as tp

from bottle import redirect, request, route, run, template

from bayes import NaiveBayesClassifier
from db import News, engine, get_session, refresh_news, update_label
from scraputils import get_news
from textutils import clean

weight = {"maybe": 1, "good": 0, "never": 2}


@tp.no_type_check
@route("/")
@route("/news")
def news_list():
    """ Display a list of unmarked news items """
    s = get_session(engine)
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@tp.no_type_check
@route("/add_label/")
def add_label():
    """ Add label to news """
    s = get_session(engine)
    r = request.query_string
    label, id = r.split("&")
    label = label.split("=")[1]
    id = id.split("=")[1]
    update_label(session=s, id=id, label=label)

    redirect("/news")


@tp.no_type_check
@route("/update")
def update_news():
    """  Add fresh news to Base """
    s = get_session(engine)
    refresh_news(s)

    redirect("/news")


@tp.no_type_check
@route("/classify")
def classify_news():
    """ Classify news using Bayes """
    s = get_session(engine)
    model = NaiveBayesClassifier()
    classified_by_hands = s.query(News).filter(News.label != None).all()
    model.fit(
        [clean(news.title).lower() for news in classified_by_hands],
        [news.label for news in classified_by_hands],
    )
    data_to_classify = s.query(News).filter(News.label == None).all()
    return template(
        "news_template",
        rows=sorted(
            data_to_classify, key=lambda news: weight[model.predict([clean(news.title).lower()])[0]]
        ),
    )


if __name__ == "__main__":
    run(host="localhost", port=8080)
