if __name__ == '__main__':
    from models.engine.db_storage import DBStorage

    storage = DBStorage()
    user = {"username": "saad", "password": "kdopewjdiwe"}
    storage.insert_one(user)
    storage.close_connection()
