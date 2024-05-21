from sqlalchemy.orm import Session
from schema.subjectSchema import SubjectSchema
from model.subject import Subject
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

# get all subjects
def get_subjects(db:Session) -> list:
        return db.query(Subject).all()


# get subject by id 
def get_subject_by_id(db:Session, subject_id:int) -> Subject:
    try:
        return db.query(Subject).filter(subject_id == Subject.id).first()
    except:
        raise HTTPException(status_code=404,detail="Error, subject not found")
    
           
# create subject
def create_subject(db:Session, subject: SubjectSchema) -> SubjectSchema:
    try:
        _subject = Subject(name = subject.name,semester = subject.semester,carrer_id = subject.carrer_id)
        db.add(_subject)
        db.commit()
        db.refresh(_subject)
        return SubjectSchema.from_orm(_subject)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Unprocessable Entity: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
    
# delete subject
def delete_subject(db:Session,subject_id:int) -> str:
    try:
        _subject = get_subject_by_id(db=db,subject_id=subject_id)
        db.delete(_subject)
        db.commit()
        return f"Subject {subject_id} Successfully deleted"
    except:
        raise HTTPException(status_code=404,detail="Error, Subject not found")
    
    
# update subject
def update_subject(db:Session, subject_id:int, name:str, semester:str, carrer_id:int) -> SubjectSchema:
    try:
        _subject = get_subject_by_id(db=db,subject_id=subject_id)
        _subject.name = name
        _subject.semester = semester
        _subject.carrer_id = carrer_id
        db.commit()
        db.refresh(_subject)
        return SubjectSchema.from_orm(_subject)
    except:
        raise HTTPException(status_code=422,detail="Unprocessable Entity")
