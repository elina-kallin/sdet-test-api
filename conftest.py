import os

import pytest
from dotenv import load_dotenv

from src.api_client import WordPressAPIClient
from src.data_base_client import WordPressDataBaseClient


load_dotenv()


@pytest.fixture(scope="session")
def config():
    return {
        "wp_base_url": os.getenv("WP_BASE_URL"),
        "wp_username": os.getenv("WP_USERNAME"),
        "wp_password": os.getenv("WP_PASSWORD"),
        "db_host": os.getenv("DB_HOST"),
        "db_port": int(os.getenv("DB_PORT")),
        "db_name": os.getenv("DB_NAME"),
        "db_user": os.getenv("DB_USER"),
        "db_password": os.getenv("DB_PASSWORD"),
        "test_author_id": int(os.getenv("TEST_AUTHOR_ID")),
    }


@pytest.fixture(scope="session")
def api_client():
    return WordPressAPIClient(
        base_url=config["wp_base_url"],
        username=config["wp_username"],
        password=["wp_password"],
    )


@pytest.fixture(scope="session")
def db_client():
    return WordPressDataBaseClient(
        host=["db_host"],
        port=["db_port"],
        database=["db_name"],
        user=["db_user"],
        password=["db_password"],
    )
