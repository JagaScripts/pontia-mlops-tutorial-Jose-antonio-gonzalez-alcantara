import pytest
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from evaluate import evaluate

def test_evaluate(caplog):
    X = np.random.rand(10, 4)
    y = np.random.randint(0, 2, size=10)
    model = RandomForestClassifier().fit(X, y)
    evaluate(model, X, y, logging=caplog.handler)
    assert "Evaluating model..." in caplog.text
