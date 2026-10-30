
import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import (
    ConnectionFailure,
    ConfigurationError,
    PyMongoError,
)

# Locate the project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Load environment variables
ENV_PATH = BASE_DIR / ".env"
load_dotenv(ENV_PATH)

# MongoDB configuration
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE = os.getenv(
    "MONGODB_DATABASE",
    "student_success_db"
)

# Reusable MongoDB client
_client = None


def get_client():
    """
    Create and return a reusable MongoDB client.
    """

    global _client

    if not MONGODB_URI:
        raise ValueError(
            "MONGODB_URI is missing. Check your .env file."
        )

    if _client is None:
        _client = MongoClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=5000
        )

    return _client


def get_database():
    """
    Connect to MongoDB Atlas and return the database.
    """

    try:
        client = get_client()

        # Verify MongoDB connection
        client.admin.command("ping")

        database = client[MONGODB_DATABASE]

        return database

    except (ConnectionFailure, ConfigurationError) as error:
        raise ConnectionError(
            f"MongoDB connection failed: {error}"
        ) from error

    except PyMongoError as error:
        raise RuntimeError(
            f"MongoDB error: {error}"
        ) from error


def close_connection():
    """
    Close the MongoDB connection.
    """

    global _client

    if _client is not None:
        _client.close()
        _client = None


def test_connection():
    """
    Test MongoDB Atlas connectivity.
    """

    try:
        database = get_database()

        print("MongoDB Atlas connected successfully!")
        print(f"Database: {database.name}")

        return True

    except Exception as error:
        print(f"MongoDB connection error: {error}")

        return False
