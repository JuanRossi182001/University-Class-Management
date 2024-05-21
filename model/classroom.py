from sqlalchemy import Column,Integer,String,Table,ForeignKey
from config.config import base
from sqlalchemy.orm import relationship

class Classroom(base):
    __tablename__ = "Classrooms"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    Hour = relationship('Hour', back_populates='Classroom')
    
    
    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "hours": [hours.__dict__ for hours in self.hours]
        }