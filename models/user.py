#!/usr/bin/python3
""" holds class User"""

import models
from models.base_model import BaseModel
from hashlib import md5


class User(BaseModel):
    """Representation of a user """

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
