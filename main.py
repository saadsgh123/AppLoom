if __name__ == '__main__':
    from models.base_model import BaseModel

    base = BaseModel(name="saad", lname="sghouri")
    print(base.to_dict())
