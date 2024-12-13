from pymongo import MongoClient


class DBStorage:
    """
    A class to handle CRUD operations for MongoDB collections.
    """

    def __init__(self, uri="mongodb://localhost:27017", database_name="apploom", collection_name="users"):
        """
        Initialize the DBStorage instance.

        Args:
            uri (str): MongoDB connection URI.
            Database_name (str): Name of the database to use.
            Collection_name (str): Name of the collection to use.
        """
        self.client = MongoClient(uri)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def insert_one(self, data):
        """
        Insert a single document into the collection.

        Args:
            data (dict): Document to insert.

        Returns:
            InsertOneResult: The result of the insert operation.
        """
        return self.collection.insert_one(data)

    def insert_many(self, data_list):
        """
        Insert multiple documents into the collection.

        Args:
            data_list (list): List of documents to insert.

        Returns:
            InsertManyResult: The result of the insert operation.
        """
        print(f"Inserting documents: {data_list}")
        return self.collection.insert_many(data_list)

    def find_one(self, query):
        """
        Retrieve a single document from the collection.

        Args:
            query (dict): Query to match the document.

        Returns:
            dict: The matched document or None if no match is found.
        """
        return self.collection.find_one(query)

    def find_all(self):
        """
        Retrieve all documents from the collection.

        Returns:
            list: List of all documents in the collection.
        """
        return list(self.collection.find())

    def update_one(self, query, update):
        """
        Update a single document in the collection.

        Args:
            query (dict): Query to match the document.
            update (dict): Update operations to apply.

        Returns:
            UpdateResult: The result of the update operation.
        """
        return self.collection.update_one(query, update)

    def delete_one(self, query):
        """
        Delete a single document from the collection.

        Args:
            query (dict): Query to match the document.

        Returns:
            DeleteResult: The result of the delete operation.
        """
        return self.collection.delete_one(query)

    def delete_many(self, query):
        """
        Delete multiple documents from the collection.

        Args:
            query (dict): Query to match the documents.

        Returns:
            DeleteResult: The result of the delete operation.
        """
        return self.collection.delete_many(query)

    def close_connection(self):
        """
        Close the MongoDB client connection.
        """
        self.client.close()
