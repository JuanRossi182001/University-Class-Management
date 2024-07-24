from sqlalchemy.orm import Session
from schema.subjectSchema import SubjectSchema,SubjectResponse
from model.subject import Subject
from typing import Annotated,List
from fastapi.param_functions import Depends
from config.db.connection import get_db
from sqlalchemy.orm.exc import NoResultFound


class SubjectService():
    
    def __init__(self, db: Annotated[Session,Depends(get_db)]) -> None:
        self.db = db

    # get all subjects
    def get_subjects(self) -> List[SubjectResponse]:
            subjects_list = self.db.query(Subject).all()
            return [SubjectResponse.model_validate(sub) for sub in subjects_list]


    # get subject by id 
    def get_subject_by_id(self, subject_id:int) -> SubjectResponse:
        _subject = self.db.query(Subject).filter(subject_id == Subject.id).first()
        if not _subject:
            raise NoResultFound(f"Error, classroom {subject_id} not found")
        return SubjectResponse.model_validate(_subject)
        
        
            
    # create subject
    def create_subject(self, subject: SubjectSchema) -> SubjectResponse:
        _subject = Subject(**subject.model_dump())
        self.db.add(_subject)
        self.db.commit()
        self.db.refresh(_subject)
        return SubjectResponse.model_validate(_subject)
       
        
    # delete subject
    def delete_subject(self,subject_id:int) -> str:
        _subject = self.get_subject_by_id(subject_id=subject_id)
        self.db.delete(_subject)
        self.db.commit()
        return _subject
            
        
        
    # update subject
    def update_subject(self, subject_id:int, name:str, semester:str, carrer_id:int) -> SubjectResponse:
            _subject = self.get_subject_by_id(subject_id=subject_id)
            _subject.name = name
            _subject.semester = semester
            _subject.carrer_id = carrer_id
            self.db.commit()
            self.db.refresh(_subject)
            return SubjectResponse.model_validate(_subject)
        
