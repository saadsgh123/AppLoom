from anyio import sleep
from bson import DBRef

from models.job_app import JobApp
from models.user import User
from models.base_model import BaseModel
from  models import storage

if __name__ == '__main__':


    user = JobApp(username="saadsgh12", firstname="saad", lastname="sghouri")
    print(storage.get_collection(JobApp()))



