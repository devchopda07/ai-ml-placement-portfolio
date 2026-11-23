"""Build an in-memory SQLite cohort report from synthetic transactions."""
import sqlite3


COHORT_QUERY = """
WITH first_activity AS (
    SELECT customer_id, MIN(strftime('%Y-%m', order_date)) AS cohort
    FROM orders
    GROUP BY customer_id
),
cohort_sizes AS (
    SELECT cohort, COUNT(*) AS customers
    FROM first_activity
    GROUP BY cohort
),
monthly_activity AS (
    SELECT f.cohort, strftime('%Y-%m', o.order_date) AS activity_month,
           COUNT(DISTINCT o.customer_id) AS active_customers
    FROM orders o
    JOIN first_activity f USING (customer_id)
    GROUP BY f.cohort, activity_month
)
SELECT m.cohort, m.activity_month, m.active_customers, c.customers,
       ROUND(100.0 * m.active_customers / c.customers, 1) AS retention_pct
FROM monthly_activity m
JOIN cohort_sizes c USING (cohort)
ORDER BY m.cohort, m.activity_month
"""


def cohort_report():
    with sqlite3.connect(":memory:") as database:
        database.execute("CREATE TABLE orders (customer_id INTEGER, order_date TEXT)")
        database.executemany(
            "INSERT INTO orders VALUES (?, ?)",
            [(1, "2025-01-01"), (2, "2025-01-14"), (1, "2025-02-02"),
             (1, "2025-02-18"), (3, "2025-02-06"), (3, "2025-03-01")],
        )
        return database.execute(COHORT_QUERY).fetchall()


if __name__ == "__main__":
    print("cohort,activity_month,active_customers,cohort_size,retention_pct")
    for row in cohort_report():
        print(",".join(map(str, row)))
