import csv
import pathlib

import bayes
import textutils


def test_classification_messages() -> None:
    x = []
    y = []

    with (pathlib.Path(__file__).parent.parent / "data/SMSSpamCollection").open() as f:
        for i, j in map(lambda x: x.split("\t"), f.readlines()):
            x.append(j)
            y.append(i)

    X_train, y_train, X_test, y_test = x[:3900], y[:3900], x[3900:], y[3900:]

    model = bayes.NaiveBayesClassifier(0.05)
    model.fit(list(map(lambda x: textutils.clean(x), X_train)), y_train)
    assert model.score(list(map(lambda x: textutils.clean(x), X_test)), y_test) > 0.97
