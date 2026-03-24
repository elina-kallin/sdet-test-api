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
def api_client(config):
    return WordPressAPIClient(
        base_url=config["wp_base_url"],
        username=config["wp_username"],
        password=config["wp_password"],
    )


@pytest.fixture(scope="session")
def db_client(config):
    return WordPressDataBaseClient(
        host=config["db_host"],
        port=config["db_port"],
        database=config["db_name"],
        user=config["db_user"],
        password=config["db_password"],
    )


@pytest.fixture
def created_post_ids():
    ids = []
    yield ids


@pytest.fixture
def created_comment_ids():
    ids = []
    yield ids
