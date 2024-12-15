from anyio import sleep

from models.job_app import JobApp
from models.user import User
from models.base_model import BaseModel

if __name__ == '__main__':


    user = JobApp(username="saadsgh12", firstname="saad", lastname="sghouri")
    print(user.to_dict())



