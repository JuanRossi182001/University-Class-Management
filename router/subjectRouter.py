from fastapi import APIRouter, HTTPException,Depends
from schema.subjectSchema import RequestSubject
from service.subjectService import SubjectService
from typing import Annotated
from fastapi import status
from sqlalchemy.orm.exc import NoResultFound

router = APIRouter()


        
dependency = Annotated[SubjectService,Depends()]      
        
        
# get all subjects end point
@router.get("/")
async def get_all(subject_service: dependency):
    _subjects = subject_service.get_subjects()
    return _subjects
        
    
    
# get subject by id end point 
@router.get("/{subject_id}")
async def get_by_id(subject_id: int,subject_service: dependency):
    try:
        _subject = subject_service.get_subject_by_id(subject_id=subject_id,)
        return _subject
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    

# create subject end point
@router.post("/create")
async def create(sub: RequestSubject, subject_service: dependency):
    _subject = subject_service.create_subject(subject=sub)
    return _subject
       

# delete subject end point
@router.delete("/delete/{subject_id}")
async def delete(subject_id: int, subject_service: dependency):
    try:
        _subject = subject_service.delete_subject(subject_id=subject_id)
        return _subject
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    
 
# update subject end point   
@router.patch("/update/{subject_id}")
async def update(subject_id: int, sub: RequestSubject , subject_service: dependency):
    try:
        _subject = subject_service.update_subject(
            subject_id=subject_id
            ,name=sub.name,
            semester=sub.semester,
            carrer_id=sub.carrer_id
            )
        return _subject
    except:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Fail to update data")