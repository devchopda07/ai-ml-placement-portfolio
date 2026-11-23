# AI/ML and SQL Placement Portfolio

Two runnable projects that show how to evaluate a model and answer a product analytics question.

## Customer churn risk

Train a logistic regression baseline on reproducible synthetic customer data. The pipeline fits feature scaling on the training split and evaluates on held-out customers. It reports average precision against the positive-rate reference, plus precision and recall at the default threshold. Synthetic results only describe this simulation.

Requires Python and scikit-learn.

```sh
python -m pip install scikit-learn
python churn_model.py --output metrics.json
```

## Customer cohort retention

Use SQLite to group customers by first order month and calculate monthly repeat activity. The query counts distinct customers, so repeat orders in one month do not inflate retention. Months with no activity are absent from this compact example.

Runs with the Python standard library.

```sh
python cohort_retention.py
```

The example shows 50% February retention for the January cohort and 100% March retention for the February cohort. All records are synthetic.
