#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user and hash the password"""

        password = kwargs.pop('password')
        md5_hash = hashlib.md5()
        md5_hash.update(password.encode())
        hashed_password = md5_hash.hexdigest()
        kwargs["password"] = hashed_password
        super().__init__(*args, **kwargs)

    def to_dict(self):
        """ overriding the to_dict() method
        """
        instance_dict = super().to_dict()
        instance_dict.pop("password")
        return instance_dict
