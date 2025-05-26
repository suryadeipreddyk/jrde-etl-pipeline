import pyodbc
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# SQL Server config
SQL_SERVER_HOST = os.getenv("SQL_SERVER_HOST", "localhost")
SQL_SERVER_PORT = os.getenv("SQL_SERVER_PORT", "1433")
SQL_SERVER_DB = os.getenv("SQL_SERVER_DB", "WarehouseDB")
SQL_SERVER_USER = os.getenv("SQL_SERVER_USER", "sa")
SQL_SERVER_PASSWORD = os.getenv("SQL_SERVER_PASSWORD", "YourStrong!Passw0rd")


def get_sql_server_connection():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SQL_SERVER_HOST},{SQL_SERVER_PORT};"
        f"DATABASE={SQL_SERVER_DB};"
        f"UID={SQL_SERVER_USER};"
        f"PWD={SQL_SERVER_PASSWORD};"
    )
    return pyodbc.connect(conn_str)


def load_to_sql_server(data):
    if not data:
        logging.info("No data to load into SQL Server.")
        return

    conn = get_sql_server_connection()
    cursor = conn.cursor()

    create_table_sql = """
    IF NOT EXISTS (
        SELECT * FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_NAME = 'FactUserPosts'
    )
    BEGIN
        CREATE TABLE FactUserPosts (
            PostID INT,
            PostTitle NVARCHAR(MAX),
            PostBody NVARCHAR(MAX),
            UserName NVARCHAR(255),
            UserEmail NVARCHAR(255)
        );
    END
    """

    insert_sql = """
    INSERT INTO FactUserPosts (PostID, PostTitle, PostBody, UserName, UserEmail)
    VALUES (?, ?, ?, ?, ?);
    """

    try:
        cursor.execute(create_table_sql)
        conn.commit()

        for row in data:
            cursor.execute(insert_sql, (
                row["post_id"],
                row["post_title"],
                row["post_body"],
                row["user_name"],
                row["user_email"]
            ))
        conn.commit()
        logging.info(f"Loaded {len(data)} records into SQL Server.")
    except Exception as e:
        logging.error(f"Error inserting into SQL Server: {e}")
    finally:
        cursor.close()
        conn.close()