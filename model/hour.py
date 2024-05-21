from config.config import base
from sqlalchemy import Integer,Column,DateTime,ForeignKey
from sqlalchemy.orm import relationship

class Hour(base):
    __tablename__ = "Hours"
    
    id = Column(Integer, primary_key=True)
    start_hour = Column(DateTime)
    end_hour = Column(DateTime)
    
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    Subject = relationship("Subject", back_populates="Hour")
    
    classroom_id = Column(Integer, ForeignKey('Classrooms.id'))
    Classroom = relationship("Classroom", back_populates="Hour")
    
    
    def as_dict(self):
        return{
            "id": self.id,
            "start_hour": self.start_hour,
            "end_hour": self.end_hour,
            "subject_id": self.subject_id,
            "classroom_id": self.classroom_id
        }