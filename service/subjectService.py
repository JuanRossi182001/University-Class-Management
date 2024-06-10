from sqlalchemy.orm import Session
from schema.subjectSchema import SubjectSchema
from model.subject import Subject
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated
from fastapi.param_functions import Depends
from router.db.connection import get_db
from sqlalchemy.orm.exc import NoResultFound


class SubjectService():
    
    def __init__(self, db: Annotated[Session,Depends(get_db)]) -> None:
        self.db = db

    # get all subjects
    def get_subjects(self) -> list:
            return self.db.query(Subject).all()


    # get subject by id 
    def get_subject_by_id(self, subject_id:int) -> Subject:
        _subject = self.db.query(Subject).filter(subject_id == Subject.id).first()
        if not _subject:
            raise NoResultFound(f"Error, classroom {subject_id} not found")
        return _subject
        
        
            
    # create subject
    def create_subject(self, subject: SubjectSchema) -> SubjectSchema:
        _subject = Subject(**subject.model_dump())
        self.db.add(_subject)
        self.db.commit()
        self.db.refresh(_subject)
        return SubjectSchema.model_validate(_subject)
       
        
    # delete subject
    def delete_subject(self,subject_id:int) -> str:
        _subject = self.get_subject_by_id(subject_id=subject_id)
        self.db.delete(_subject)
        self.db.commit()
        return _subject
            
        
        
    # update subject
    def update_subject(self, subject_id:int, name:str, semester:str, carrer_id:int) -> SubjectSchema:
            _subject = self.get_subject_by_id(subject_id=subject_id)
            _subject.name = name
            _subject.semester = semester
            _subject.carrer_id = carrer_id
            self.db.commit()
            self.db.refresh(_subject)
            return SubjectSchema.model_validate(_subject)
        
