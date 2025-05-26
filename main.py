from etl.extract import get_users, get_posts
from etl.load import create_staging_tables, load_users, load_posts
from etl.transform import transform_data
from etl.warehousing import load_to_sql_server
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    logging.info("ETL Pipeline started")

    # 1. Extract
    users = get_users()
    posts = get_posts()
    if not users or not posts:
        logging.error("Extraction failed, aborting pipeline")
        return

    # 2. Load to PostgreSQL staging
    create_staging_tables()
    load_users(users)
    load_posts(posts)

    # 3. Transform
    transformed = transform_data()
    if not transformed:
        logging.error("Transformation failed, aborting pipeline")
        return

    # 4. Load to SQL Server warehouse
    load_to_sql_server(transformed)

    logging.info("ETL Pipeline completed successfully")


if __name__ == "__main__":
    main()