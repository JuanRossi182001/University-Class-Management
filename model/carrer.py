from config.config import base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship

class Carrer(base):
    __tablename__ = "carrers"
    
    id = Column(Integer,primary_key=True)
    name = Column(String)
    duration_in_years = Column(Integer)
    
    subjects = relationship('Subject', back_populates='carrer')
    
    
    def as_dict(self):
        return{
            "name": self.name,
            "duration_in_years": self.duration_in_years,
            "subjects": self.subjects
        } 