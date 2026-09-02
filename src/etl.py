import pandas as pd
from getpass import getpass
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# -----------------------------
# 1. DATABASE CONNECTION
# -----------------------------

password = getpass("Enter MySQL password: ")

connection_url = URL.create(
    drivername="mysql+mysqlconnector",
    username="root",
    password=password,
    host="localhost",
    port=3306,
    database="business_analytics"
)

engine = create_engine(connection_url)

print("MySQL connection successful")


# -----------------------------
# 2. EXTRACT
# -----------------------------

sales = pd.read_sql(
    "SELECT * FROM sales",
    engine
)

print(f"Sales rows extracted: {len(sales)}")


# -----------------------------
# 3. CLEAN
# -----------------------------

sales = sales.drop_duplicates()

sales["sale_date"] = pd.to_datetime(
    sales["sale_date"],
    errors="coerce"
)

numeric_columns = [
    "quantity",
    "unit_price",
    "total_amount"
]

for column in numeric_columns:
    sales[column] = pd.to_numeric(
        sales[column],
        errors="coerce"
    )

sales = sales.dropna(
    subset=[
        "sale_id",
        "customer_id",
        "product_id",
        "sale_date",
        "quantity",
        "unit_price",
        "total_amount"
    ]
)

sales = sales[
    (sales["quantity"] > 0) &
    (sales["unit_price"] >= 0) &
    (sales["total_amount"] >= 0)
]


# -----------------------------
# 4. FEATURE ENGINEERING
# -----------------------------

sales["year"] = sales["sale_date"].dt.year
sales["month"] = sales["sale_date"].dt.month
sales["month_name"] = sales["sale_date"].dt.month_name()


# -----------------------------
# 5. VALIDATION
# -----------------------------

print(f"Clean rows: {len(sales)}")
print(f"Duplicate rows remaining: {sales.duplicated().sum()}")
print(f"Missing values remaining: {sales.isna().sum().sum()}")


# -----------------------------
# 6. SAVE CLEANED CSV
# -----------------------------

output_path = "data/processed/sales_cleaned.csv"

sales.to_csv(
    output_path,
    index=False
)

print(f"Processed data saved to: {output_path}")


# -----------------------------
# 7. LOAD CLEAN DATA TO MYSQL
# -----------------------------

sales.to_sql(
    name="sales_cleaned",
    con=engine,
    if_exists="replace",
    index=False
)

print("Cleaned data loaded into MySQL table: sales_cleaned")

print("\nETL pipeline completed successfully.")