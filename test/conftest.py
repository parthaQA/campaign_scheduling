import pytest
from pymongo import MongoClient

MONGO_URI = "mongodb://root:root@localhost:27017/admin"  # Update credentials if necessary
DATABASE_NAME = "campaign-scheduling"
COLLECTION_NAME = "campaign"


@pytest.fixture(scope="class")
def mongo_client(request):
    """Fixture to establish a MongoDB connection."""
    global client
    try:
        # Establish connection
        client = MongoClient(MONGO_URI)
        databases = client.list_database_names()
        print(databases)
        # Access the admin database and verify connection
        db_admin = client[DATABASE_NAME]
        assert db_admin.command("ping")["ok"] == 1.0, "Failed to connect to MongoDB"
        print("Connected to MongoDB", db_admin.command("ping")["ok"])
        # Attach the client and db_admin to the test class
        request.cls.client = client
        request.cls.db_admin = db_admin
        yield db_admin  # Provide the fixture for tests
    finally:
        # ✅ Close connection after tests are done
        client.close()
