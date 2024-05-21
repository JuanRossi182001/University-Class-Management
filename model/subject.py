from config.config import base
from sqlalchemy import Integer,String,Column,Table,ForeignKey
from sqlalchemy.orm import relationship


class Subject(base):
    __tablename__ = "subjects"
    
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    semester = Column(String)
    
    carrer_id = Column(Integer, ForeignKey('carrers.id'))
    carrer = relationship('Carrer', back_populates='subjects')
    Hour = relationship('Hour', back_populates='Subject')
    
    def as_dict(self):
        return {
            "name": self.name,
            "carrer": [carrer.as_dict() for carrer in self.carrers],
            "semester": self.semester
        }