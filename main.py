from anyio import sleep

from models.user import User
from models.base_model import BaseModel

if __name__ == '__main__':


    user = User(username="saadsgh12", firstname="saad", lastname="sghouri")
    print(user)
    user1 = User(**user.to_dict())
    user1.slm = 45
    print(user1)


