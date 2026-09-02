import os
import socket
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env")


# =========================================================
# FORCE IPV4 CONNECTION
# =========================================================

_original_getaddrinfo = socket.getaddrinfo


def ipv4_only_getaddrinfo(
    host,
    port,
    family=0,
    type=0,
    proto=0,
    flags=0
):
    return _original_getaddrinfo(
        host,
        port,
        socket.AF_INET,
        type,
        proto,
        flags
    )


socket.getaddrinfo = ipv4_only_getaddrinfo


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(
        timeout=10000,
        retry_options=types.HttpRetryOptions(
            attempts=1
        )
    )
)

MODEL = "gemini-3.5-flash-lite"


# =========================================================
# DATABASE SCHEMA
# =========================================================

DATABASE_SCHEMA = """

DATABASE: business_analytics


TABLE: sales_cleaned

COLUMNS:
- sale_id
- customer_id
- product_id
- quantity
- region
- sale_date
- payment_method
- total_amount
- unit_price


TABLE: products

COLUMNS:
- product_id
- product_name
- category
- sub_category
- unit_cost
- selling_price


TABLE: customers

COLUMNS:
- customer_id
- customer_name
- email
- city
- region
- customer_segment
- registration_date


RELATIONSHIPS:

sales_cleaned.product_id = products.product_id

sales_cleaned.customer_id = customers.customer_id

"""


# =========================================================
# SQL GENERATOR
# =========================================================

def generate_sql(question):

    prompt = f"""

You are a Senior Data Analyst and MySQL SQL Developer.

Convert the user's natural-language business question
into a correct MySQL SQL query.

DATABASE SCHEMA:

{DATABASE_SCHEMA}


BUSINESS DEFINITIONS:

Revenue:
SUM(sales_cleaned.total_amount)

Units Sold:
SUM(sales_cleaned.quantity)

Transactions:
COUNT(DISTINCT sales_cleaned.sale_id)

Average Transaction Value:
AVG(sales_cleaned.total_amount)


=========================================================
SQL SAFETY RULES
=========================================================

1. Return ONLY SQL.

2. Use MySQL syntax.

3. Only generate SELECT or WITH queries.

4. NEVER generate:

INSERT
UPDATE
DELETE
DROP
ALTER
TRUNCATE
CREATE
GRANT
REVOKE


=========================================================
PRODUCT QUESTIONS
=========================================================

When the user asks about products,
JOIN the products table.

Example:

Question:
Which product generated the highest revenue?

SQL:

SELECT
    p.product_name,
    SUM(s.total_amount) AS revenue
FROM sales_cleaned s
JOIN products p
    ON s.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name
ORDER BY revenue DESC
LIMIT 1;


For all products:

SELECT
    p.product_name,
    SUM(s.total_amount) AS revenue
FROM sales_cleaned s
JOIN products p
    ON s.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name
ORDER BY revenue DESC;


For product categories:

SELECT
    p.category,
    SUM(s.total_amount) AS revenue
FROM sales_cleaned s
JOIN products p
    ON s.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;


=========================================================
CUSTOMER QUESTIONS
=========================================================

When the user asks about customers,
JOIN the customers table.

Example:

Question:
Which customer generated the highest revenue?

SQL:

SELECT
    c.customer_name,
    SUM(s.total_amount) AS revenue
FROM sales_cleaned s
JOIN customers c
    ON s.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY revenue DESC
LIMIT 1;


For top 5 customers:

SELECT
    c.customer_name,
    SUM(s.total_amount) AS revenue
FROM sales_cleaned s
JOIN customers c
    ON s.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY revenue DESC
LIMIT 5;


=========================================================
CUSTOMER SEGMENT QUESTIONS
=========================================================

For customer segment analysis:

SELECT
    c.customer_segment,
    SUM(s.total_amount) AS revenue
FROM sales_cleaned s
JOIN customers c
    ON s.customer_id = c.customer_id
GROUP BY c.customer_segment
ORDER BY revenue DESC;


=========================================================
CITY QUESTIONS
=========================================================

For revenue by city:

SELECT
    c.city,
    SUM(s.total_amount) AS revenue
FROM sales_cleaned s
JOIN customers c
    ON s.customer_id = c.customer_id
GROUP BY c.city
ORDER BY revenue DESC;


=========================================================
REGION QUESTIONS
=========================================================

For revenue by region:

SELECT
    region,
    SUM(total_amount) AS revenue
FROM sales_cleaned
GROUP BY region
ORDER BY revenue DESC;


For highest revenue region:

SELECT
    region,
    SUM(total_amount) AS revenue
FROM sales_cleaned
GROUP BY region
ORDER BY revenue DESC
LIMIT 1;


=========================================================
MONTHLY REVENUE
=========================================================

For monthly revenue:

SELECT
    DATE_FORMAT(sale_date, '%Y-%m') AS sale_month,
    SUM(total_amount) AS revenue
FROM sales_cleaned
GROUP BY sale_month
ORDER BY sale_month;


=========================================================
PAYMENT METHOD
=========================================================

For revenue by payment method:

SELECT
    payment_method,
    SUM(total_amount) AS revenue
FROM sales_cleaned
GROUP BY payment_method
ORDER BY revenue DESC;


=========================================================
GENERAL RULES
=========================================================

1. For highest/lowest/top/bottom questions,
return BOTH the category and metric.

2. Use meaningful aliases:

revenue
total_units
transactions
average_transaction_value

3. When a name is available, prefer the name instead
of displaying an ID.

4. Never invent columns.

5. Use only the provided tables and columns.

6. Use JOINs when required.

7. Do not explain the query.

8. Do not use Markdown.

9. Do not use code fences.

10. Return SQL only.


USER BUSINESS QUESTION:

{question}

"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    sql = response.text.strip()

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")

    return sql.strip()


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    question = input(
        "Enter your business question: "
    )

    try:

        sql = generate_sql(question)

        print("\nGenerated SQL:")
        print("-" * 50)
        print(sql)

    except Exception as error:

        print("\nERROR:")
        print(error)