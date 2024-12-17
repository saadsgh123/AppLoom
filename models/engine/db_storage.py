from pymongo import MongoClient
from models.base_model import BaseModel


class DBStorage:
    """
    A class to handle CRUD operations for MongoDB collections.
    """

    def __init__(self, uri="mongodb://localhost:27017", database_name="apploom"):
        """
        Initialize the DBStorage instance.

        Args:
            uri (str): MongoDB connection URI.
            database_name (str): Name of the database to use.
        """
        self.client = MongoClient(uri)
        self.db = self.client[database_name]
        self.collections = {
            'User': self.db['users'],
            'JobApp': self.db['jobapps']
        }

    def insert_one(self, data: BaseModel):
        """
        Insert a single document into the corresponding collection.

        Args:
            data (BaseModel): Instance of BaseModel to insert.

        Returns:
            InsertOneResult: The result of the insert operation.
        """
        collection = self._get_collection(data)
        return collection.insert_one(data.to_dict())

    def insert_many(self, data_list, model_class):
        """
        Insert multiple documents into the corresponding collection.

        Args:
            data_list (list): List of dictionaries to insert.
            model_class (type): Class of the data being inserted.

        Returns:
            InsertManyResult: The result of the insert operation.
        """
        collection = self._get_collection(model_class)
        return collection.insert_many(data_list)

    def find_one(self, model_class, query):
        """
        Retrieve a single document from the corresponding collection.

        Args:
            model_class (type): Class of the data being queried.
            query (dict): Query to match the document.

        Returns:
            dict: The matched document or None if no match is found.
        """
        collection = self._get_collection(model_class)
        return collection.find_one(query)

    def find_all(self, model_class):
        """
        Retrieve all documents from the corresponding collection.

        Args:
            model_class (type): Class of the data being queried.

        Returns:
            list: List of all documents in the collection.
        """
        collection = self._get_collection(model_class)
        return list(collection.find())

    def update_one(self, model_class, query, update):
        """
        Update a single document in the corresponding collection.

        Args:
            model_class (type): Class of the data being updated.
            query (dict): Query to match the document.
            update (dict): Update operations to apply.

        Returns:
            UpdateResult: The result of the update operation.
        """
        collection = self._get_collection(model_class)
        return collection.update_one(query, update)

    def delete_one(self, model_class, query):
        """
        Delete a single document from the corresponding collection.

        Args:
            model_class (type): Class of the data being deleted.
            query (dict): Query to match the document.

        Returns:
            DeleteResult: The result of the delete operation.
        """
        collection = self._get_collection_by_class(model_class)
        return collection.delete_one(query)

    def delete_many(self, model_class, query):
        """
        Delete multiple documents from the corresponding collection.

        Args:
            model_class (type): Class of the data being deleted.
            query (dict): Query to match the documents.

        Returns:
            DeleteResult: The result of the delete operation.
        """
        collection = self._get_collection(model_class)
        return collection.delete_many(query)

    def close_connection(self):
        """
        Close the MongoDB client connection.
        """
        self.client.close()

    def _get_collection(self, data: BaseModel):
        """
        Retrieve the collection corresponding to the data's class.

        Args:
            data (BaseModel): Instance of BaseModel.

        Returns:
            Collection: MongoDB collection.
        """
        class_name = data.__class__.__name__
        return self.collections.get(class_name)

    def _get_collection_by_class(self, model_class: BaseModel):
        """
        Retrieve the collection corresponding to the given class.

        Args:
            model_class (type): Class of the data.

        Returns:
            Collection: MongoDB collection.
        """
        class_name = model_class.__class__.__name__
        return self.collections.get(class_name)
