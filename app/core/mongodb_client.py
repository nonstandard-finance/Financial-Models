from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from typing import Dict, Any, List, Optional, Union

from app.core.constants import MONGO_DB_URL


class MongoDBClient:
    """
    A comprehensive MongoDB client with reusable methods for common database operations
    """

    _instance = None

    def __new__(cls, uri: str = MONGO_DB_URL, db_name: str = "books_db"):
        """
        Singleton pattern implementation to ensure only one MongoDB client is created

        :param uri: MongoDB connection URI
        :param db_name: Name of the database to use
        """
        if not cls._instance:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
            cls._instance._initialize(uri, db_name)
        return cls._instance

    def _initialize(self, uri: str, db_name: str):
        """
        Initialize the MongoDB client

        :param uri: MongoDB connection URI
        :param db_name: Name of the database
        """
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            self.uri = uri
            self.db_name = db_name
        except Exception as e:
            print(f"Error initializing MongoDB client: {e}")
            raise

    def get_collection(self, collection_name: str) -> Collection:
        """
        Get a specific collection

        :param collection_name: Name of the collection
        :return: MongoDB collection
        """
        return self.db[collection_name]

    def insert_document(self, collection_name: str, document: Dict[str, Any]) -> str:
        """
        Insert a single document into a collection

        :param collection_name: Name of the collection
        :param document: Document to insert
        :return: Inserted document's ID
        """
        collection = self.get_collection(collection_name)
        result = collection.insert_one(document)
        return str(result.inserted_id)

    def upsert_document(
        self,
        collection_name: str,
        filter_query: Dict[str, Any],
        update_document: Dict[str, Any],
    ) -> str:
        """
        Update a document if exists, otherwise insert

        :param collection_name: Name of the collection
        :param filter_query: Query to find the document
        :param update_document: Document to update or insert
        :return: Document ID
        """
        collection = self.get_collection(collection_name)
        result = collection.update_one(
            filter_query, {"$set": update_document}, upsert=True
        )
        return str(result.upserted_id) if result.upserted_id else None

    def find_one_document(
        self, collection_name: str, query: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Find a single document matching the query

        :param collection_name: Name of the collection
        :param query: Search query
        :return: Matching document or None
        """
        collection = self.get_collection(collection_name)
        return collection.find_one(query)

    def find_documents(
        self,
        collection_name: str,
        query: Dict[str, Any] = None,
        projection: Dict[str, Any] = None,
        limit: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Find documents matching the query

        :param collection_name: Name of the collection
        :param query: Search query
        :param projection: Fields to return
        :param limit: Maximum number of documents to return
        :return: List of matching documents
        """
        collection = self.get_collection(collection_name)
        return list(collection.find(query or {}, projection).limit(limit))

    def delete_document(self, collection_name: str, query: Dict[str, Any]) -> int:
        """
        Delete documents matching the query

        :param collection_name: Name of the collection
        :param query: Deletion query
        :return: Number of documents deleted
        """
        collection = self.get_collection(collection_name)
        result = collection.delete_many(query)
        return result.deleted_count

    def close_connection(self):
        """
        Close the MongoDB client connection
        """
        if hasattr(self, "client"):
            self.client.close()

    def __del__(self):
        """
        Ensure connection is closed when the object is deleted
        """
        self.close_connection()
