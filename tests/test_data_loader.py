import pytest
import pandas as pd
from data_loader import load_data, preprocess_data

def test_load_data(tmp_path, caplog):
    sample_data = (
        "39, State-gov, 77516, Bachelors, 13, Never-married, Adm-clerical, "
        "Not-in-family, White, Male, 2174, 0, 40, United-States, <=50K\n"
    )
    train_path = tmp_path / "adult.data"
    test_path = tmp_path / "adult.tests"
    train_path.write_text(sample_data)
    test_path.write_text("income\n" + sample_data)

    train_df, test_df = load_data(train_path, test_path, logging=caplog.handler)
    assert not train_df.empty
    assert not test_df.empty

def test_preprocess_data(caplog):
    df = pd.DataFrame({
        "age": [25, 32],
        "workclass": ["Private", "Self-emp"],
        "fnlwgt": [77516, 83311],
        "education": ["Bachelors", "HS-grad"],
        "education-num": [13, 9],
        "marital-status": ["Never-married", "Married-civ-spouse"],
        "occupation": ["Tech-support", "Craft-repair"],
        "relationship": ["Not-in-family", "Husband"],
        "race": ["White", "Black"],
        "sex": ["Male", "Female"],
        "capital-gain": [0, 0],
        "capital-loss": [0, 0],
        "hours-per-week": [40, 50],
        "native-country": ["United-States", "Cuba"],
        "income": [">50K", "<=50K"]
    })
    X_train, X_test, y_train, y_test, scaler, encoders = preprocess_data(df, df, logging=caplog.handler)
    assert X_train.shape == X_test.shape
    assert y_train.shape == y_test.shape
