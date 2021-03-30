import typing as tp

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.engine.mock import MockConnection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from scraputils import get_news

Base = declarative_base()
bd_url = "sqlite:///news.db"
engine = create_engine(bd_url, connect_args={"check_same_thread": False})
local_session = sessionmaker(autocommit=False, autoflush=False)


class News(Base):  # type:ignore
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    points = Column(Integer)
    label = Column(String)


def get_session(engine: MockConnection) -> Session:
    """ Create a session """
    local_session.configure(bind=engine)
    return local_session()


def record_news(session: Session, news_list: tp.List[tp.Dict[str, tp.Union[int, str]]]) -> None:
    """ Record news in Base """
    news = [News(**news_data) for news_data in news_list]
    session.add_all(news)
    session.commit()


def update_label(session: Session, id: int, label: str) -> None:
    """ Update label """
    entry = session.query(News).get(id)
    entry.label = label
    session.commit()


def refresh_news(session: Session) -> None:
    """ Add fresh news in Base """
    fresh_news = []
    all_news = get_news(url="https://news.ycombinator.com/newest", n_pages=1)
    for item in all_news:
        title = item["title"]
        author = item["author"]
        already_exists = list(
            session.query(News).filter(News.title == title, News.author == author)
        )
        if not already_exists:
            fresh_news.append(item)
    record_news(session, fresh_news)


Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    record_news(get_session(engine), get_news("https://news.ycombinator.com/newest", 3))
