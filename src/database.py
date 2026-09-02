import mysql.connector
import pandas as pd


DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "database": "business_analytics",
}


def execute_sql(sql, password):

    connection = mysql.connector.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=password,
        database=DB_CONFIG["database"],
    )

    try:
        df = pd.read_sql(sql, connection)
        return df

    finally:
        connection.close()