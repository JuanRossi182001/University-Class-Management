from config.config import base
from sqlalchemy import Integer,Column,ForeignKey,TIMESTAMP
from sqlalchemy.orm import relationship

class Hour(base):
    __tablename__ = "Hours"
    
    id = Column(Integer, primary_key=True)
    start_hour = Column(TIMESTAMP(timezone=True))
    end_hour = Column(TIMESTAMP(timezone=True))
    
    subject_id = Column(Integer, ForeignKey('Subjects.id'))
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