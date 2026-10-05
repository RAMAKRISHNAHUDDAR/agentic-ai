import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


DATA_PATH = "data/students.csv"

FEATURES = [
    "attendance",
    "marks",
    "assignments",
    "backlogs",
]

TARGET = "risk_label"


def load_data():
    """Load student data from CSV."""
    return pd.read_csv(DATA_PATH)


def train_model():
    """Train the student risk prediction model."""
    df = load_data()

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    return model, X_test, y_test


def evaluate_model(model, X_test, y_test):
    """Evaluate the trained model."""
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    matrix = confusion_matrix(y_test, y_pred)

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "confusion_matrix": matrix,
    }


def predict_risk(model, student_data):
    """Predict risk for one student."""
    features = pd.DataFrame(
        [{
            "attendance": student_data["attendance"],
            "marks": student_data["marks"],
            "assignments": student_data["assignments"],
            "backlogs": student_data["backlogs"],
        }]
    )

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    return {
        "prediction": int(prediction),
        "risk_probability": float(probability),
    }


if __name__ == "__main__":
    model, X_test, y_test = train_model()

    results = evaluate_model(model, X_test, y_test)

    print("Student Risk Prediction Model")
    print("--------------------------------")
    print(f"Accuracy:  {results['accuracy']:.4f}")
    print(f"Precision: {results['precision']:.4f}")
    print(f"Recall:    {results['recall']:.4f}")
    print(f"F1 Score:  {results['f1_score']:.4f}")

    print()
    print("Confusion Matrix")
    print("----------------")
    print(results["confusion_matrix"])

    print()
    print("Feature Coefficients")
    print("--------------------")

    for feature, coefficient in zip(
        FEATURES,
        model.coef_[0],
    ):
        direction = (
            "increases risk"
            if coefficient > 0
            else "decreases risk"
        )

        print(
            f"{feature}: "
            f"{coefficient:.4f} "
            f"({direction})"
        )