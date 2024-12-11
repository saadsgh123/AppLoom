#!/usr/bin/python3
""" holds class User"""

import models
from models.base_model import BaseModel
from hashlib import md5


class JobApp(BaseModel):
    """Representation of a user """

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
