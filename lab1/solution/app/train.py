"""Train a tiny iris classifier and persist it to disk.

Run once at build time (or container start) to produce model.joblib.
"""
from pathlib import Path

import joblib
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

MODEL_PATH = Path(__file__).parent / "model.joblib"


def train_and_save() -> None:
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target
    )

    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)

    accuracy = clf.score(X_test, y_test)
    print(f"Test accuracy: {accuracy:.3f}")

    joblib.dump(
        {"model": clf, "target_names": list(iris.target_names), "feature_names": list(iris.feature_names)},
        MODEL_PATH,
    )
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    train_and_save()
