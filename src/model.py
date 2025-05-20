from sklearn.ensemble import RandomForestClassifier

def train_model(X_train, y_train, logging):
    logging.info("Training RandomForestClassifier...")
    model = RandomForestClassifier(random_state=42)
    logging.info(f"Model parameters: {model.get_params()}")
    model.fit(X_train, y_train)
    return model
