import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    current = dt.datetime.now()
    response = get_friends(user_id, fields=["bdate"])
    ages = []
    friend: tp.Dict[str, tp.Any]
    for friend in response.items:  # type: ignore
        if "bdate" not in friend:
            continue
        bdate = friend["bdate"]
        if len(bdate) > 6:
            day, month, year = bdate.split(".")
            day = int(day)
            month = int(month)
            year = int(year)
        else:
            continue
        if (current.month > month) or (current.month == month and current.day > day):
            age = current.year - year
        else:
            age = current.year - year - 1
        ages.append(age)
    if not ages:
        return None
    else:
        return statistics.median(ages)
