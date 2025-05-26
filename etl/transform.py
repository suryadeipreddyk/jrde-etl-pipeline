import psycopg2
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# PostgreSQL config
PG_HOST = os.getenv("POSTGRES_HOST")
PG_PORT = os.getenv("POSTGRES_PORT")
PG_DB = os.getenv("POSTGRES_DB")
PG_USER = os.getenv("POSTGRES_USER")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD")


def get_pg_connection():
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD
    )


def transform_data():
    """Fetch joined and selected data from staging tables."""
    conn = get_pg_connection()
    cur = conn.cursor()

    query = """
        SELECT 
            p.id AS post_id,
            p.title AS post_title,
            p.body AS post_body,
            u.name AS user_name,
            u.email AS user_email
        FROM staging_posts p
        JOIN staging_users u ON p.userId = u.id;
    """

    try:
        cur.execute(query)
        rows = cur.fetchall()
        transformed = [
            {
                "post_id": row[0],
                "post_title": row[1],
                "post_body": row[2],
                "user_name": row[3],
                "user_email": row[4]
            }
            for row in rows
        ]
        logging.info(f"Transformed {len(transformed)} records")
        return transformed
    except Exception as e:
        logging.error(f"Error transforming data: {e}")
        return []
    finally:
        cur.close()
        conn.close()