import typing as tp

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine.mock import MockConnection
from sqlalchemy.orm import Session

from db import Base, News, get_session, record_news, refresh_news, update_label


def db_set_up(engine: MockConnection) -> None:
    Base.metadata.create_all(bind=engine)


def db_tear_down(session: Session) -> None:
    session.query(News).delete()
    session.commit()
    session.close()


@tp.no_type_check
@pytest.fixture
def engine() -> MockConnection:
    return create_engine("sqlite://")


@tp.no_type_check
@pytest.fixture
def session(engine: MockConnection):
    session = get_session(engine)
    db_set_up(engine)
    yield session
    db_tear_down(session)


MOCK_NEWS: tp.List[tp.Dict[str, tp.Union[int, str]]] = [
    {"title": "I have got A in programming", "url": "example.com", "points": 2, "author": "Asya"},
    {
        "title": "We have ended this university",
        "url": "example.ru",
        "points": 37,
        "author": "Somebody",
    },
]


def test_record_news(session: Session) -> None:
    record_news(session=session, news_list=MOCK_NEWS)

    recorded_item = session.query(News).get(1)
    assert recorded_item.title == MOCK_NEWS[0]["title"]
    assert recorded_item.author == MOCK_NEWS[0]["author"]
    assert recorded_item.points == MOCK_NEWS[0]["points"]
    assert recorded_item.url == MOCK_NEWS[0]["url"]

    recorded_item = session.query(News).get(2)
    assert recorded_item.title == MOCK_NEWS[1]["title"]
    assert recorded_item.author == MOCK_NEWS[1]["author"]
    assert recorded_item.points == MOCK_NEWS[1]["points"]
    assert recorded_item.url == MOCK_NEWS[1]["url"]


def test_update_label(session: Session) -> None:
    record_news(session=session, news_list=MOCK_NEWS)
    update_label(session=session, id=1, label="Interesting")
    item_id = session.query(News).get(1)
    assert item_id.label == "Interesting"


def test_refresh_news(session: Session) -> None:
    try:
        refresh_news(session=session)
    except Exception:
        assert False
    fresh_item = session.query(News).all()
    assert fresh_item
