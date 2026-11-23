"""Train and evaluate a churn model on a reproducible synthetic dataset."""
import argparse
import json
import random
from pathlib import Path

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def generate_customers(seed=42, count=2000):
    rng = random.Random(seed)
    features, labels = [], []
    for _ in range(count):
        tenure = rng.randint(1, 60)
        tickets = rng.randint(0, 8)
        weekly_sessions = rng.randint(0, 25)
        risk = .10 + .045 * tickets - .002 * tenure - .003 * weekly_sessions
        features.append([tenure, tickets, weekly_sessions])
        labels.append(int(rng.random() < risk))
    return features, labels


def evaluate(seed):
    features, labels = generate_customers(seed)
    train_x, test_x, train_y, test_y = train_test_split(
        features, labels, stratify=labels, test_size=.25, random_state=seed
    )
    pipeline = make_pipeline(StandardScaler(), LogisticRegression(random_state=seed))
    pipeline.fit(train_x, train_y)
    scores = pipeline.predict_proba(test_x)[:, 1]
    predictions = pipeline.predict(test_x)
    return {
        "seed": seed,
        "train_size": len(train_y),
        "test_size": len(test_y),
        "positive_rate": sum(test_y) / len(test_y),
        "average_precision": average_precision_score(test_y, scores),
        "precision_at_default_threshold": precision_score(test_y, predictions, zero_division=0),
        "recall_at_default_threshold": recall_score(test_y, predictions, zero_division=0),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = json.dumps(evaluate(args.seed), indent=2)
    if args.output:
        args.output.write_text(report + "\n", encoding="utf-8")
    print(report)
