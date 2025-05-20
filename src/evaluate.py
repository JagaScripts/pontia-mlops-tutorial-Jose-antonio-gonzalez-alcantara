from sklearn.metrics import accuracy_score, classification_report

def evaluate(model, X_test, y_test, logging):
    logging.info("Evaluating model...")
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    report = classification_report(y_test, preds)
    logging.info(f"Test Accuracy: {acc:.4f}")
    logging.info(f"Classification Report:\n{report}")
    return