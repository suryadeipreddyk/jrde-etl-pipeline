import psycopg2
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL connection config
PG_HOST = os.getenv("POSTGRES_HOST")
PG_PORT = os.getenv("POSTGRES_PORT")
PG_DB = os.getenv("POSTGRES_DB")
PG_USER = os.getenv("POSTGRES_USER")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_pg_connection():
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD
    )

def create_staging_tables():
    conn = get_pg_connection()
    cur = conn.cursor()

    create_users = """
    CREATE TABLE IF NOT EXISTS staging_users (
        id INT PRIMARY KEY,
        name TEXT,
        username TEXT,
        email TEXT,
        phone TEXT,
        website TEXT,
        street TEXT,
        suite TEXT,
        city TEXT,
        zipcode TEXT,
        company_name TEXT
    );
    """

    create_posts = """
    CREATE TABLE IF NOT EXISTS staging_posts (
        id INT PRIMARY KEY,
        userId INT,
        title TEXT,
        body TEXT
    );
    """

    try:
        cur.execute(create_users)
        cur.execute(create_posts)
        conn.commit()
        logging.info("Staging tables created successfully")
    except Exception as e:
        logging.error(f"Error creating staging tables: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def load_users(data):
    conn = get_pg_connection()
    cur = conn.cursor()

    insert_query = """
    INSERT INTO staging_users (
        id, name, username, email, phone, website,
        street, suite, city, zipcode, company_name
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;
    """

    try:
        for user in data:
            cur.execute(insert_query, (
                user["id"],
                user["name"],
                user["username"],
                user["email"],
                user["phone"],
                user["website"],
                user["address"]["street"],
                user["address"]["suite"],
                user["address"]["city"],
                user["address"]["zipcode"],
                user["company"]["name"]
            ))
        conn.commit()
        logging.info("User data loaded successfully")
    except Exception as e:
        logging.error(f"Error loading user data: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def load_posts(data):
    conn = get_pg_connection()
    cur = conn.cursor()

    insert_query = """
    INSERT INTO staging_posts (id, userId, title, body)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;
    """

    try:
        for post in data:
            cur.execute(insert_query, (
                post["id"],
                post["userId"],
                post["title"],
                post["body"]
            ))
        conn.commit()
        logging.info("Post data loaded successfully")
    except Exception as e:
        logging.error(f"Error loading post data: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()