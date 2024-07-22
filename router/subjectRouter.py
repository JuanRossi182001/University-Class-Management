from fastapi import APIRouter, HTTPException,Depends
from schema.subjectSchema import RequestSubject
from service.subjectService import SubjectService
from typing import Annotated
from fastapi import status
from sqlalchemy.orm.exc import NoResultFound
from service.tokenHandler import TokenHandler
from model.role import Role
from model.user import User
from service.userService import get_current_user

router = APIRouter()


        
dependency = Annotated[SubjectService,Depends()]
user_dependency = Annotated[User,Depends(get_current_user)]      
        
        
# get all subjects end point
@router.get("/")
@TokenHandler.role_required([Role.ADMIN,Role.STUDENT,Role.TEACHER])
async def get_all(user:user_dependency,subject_service: dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authentication failed")
    _subjects = subject_service.get_subjects()
    return _subjects
        
    
    
# get subject by id end point 
@router.get("/{subject_id}")
@TokenHandler.role_required([Role.ADMIN,Role.STUDENT,Role.TEACHER])
async def get_by_id(user:user_dependency,subject_id: int,subject_service: dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authentication failed")
    try:
        _subject = subject_service.get_subject_by_id(subject_id=subject_id,)
        return _subject
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    

# create subject end point
@router.post("/create")
@TokenHandler.role_required([Role.ADMIN])
async def create(user:user_dependency,sub: RequestSubject, subject_service: dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authentication failed")
    _subject = subject_service.create_subject(subject=sub)
    return _subject
       

# delete subject end point
@router.delete("/delete/{subject_id}")
@TokenHandler.role_required([Role.ADMIN])
async def delete(user:user_dependency,subject_id: int, subject_service: dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authentication failed")
    try:
        _subject = subject_service.delete_subject(subject_id=subject_id)
        return _subject
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    
 
# update subject end point   
@router.patch("/update/{subject_id}")
@TokenHandler.role_required([Role.ADMIN])
async def update(user:user_dependency,subject_id: int, sub: RequestSubject , subject_service: dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authentication failed")
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