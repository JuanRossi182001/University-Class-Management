from config.config import base
from sqlalchemy import Integer,Column,String



class User(base):
    __tablename__ = "Users"
    
    id = Column(Integer,primary_key=True)
    username = Column(String)
    password = Column(String)