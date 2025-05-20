import pytest
import numpy as np
from model import train_model

def test_train_model(caplog):
    X = np.random.rand(10, 4)
    y = np.random.randint(0, 2, size=10)
    trained_model = train_model(X, y, logging=caplog.handler)
    assert hasattr(trained_model, "predict")
