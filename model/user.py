from config.config import base
from sqlalchemy import Integer,Column,ARRAY,String
from sqlalchemy.orm import Mapped
from model.role import Role




class User(base):
    __tablename__ = "Users"
    
    id = Column(Integer,primary_key=True)
    username = Column(String)
    password = Column(String)
    role_id: Mapped[Role] = Column(ARRAY(Integer)) 



