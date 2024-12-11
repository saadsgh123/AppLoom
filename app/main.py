if __name__ == '__main__':
    from models.engine.db_storage import client

    db = client["saad"]
    collection = db["users"]
    user = {"username": "saad", "password": "<PASSWORD>"}
    collection.insert_one()
