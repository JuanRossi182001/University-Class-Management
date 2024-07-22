from fastapi import APIRouter, HTTPException,Depends
from schema.classroomSchema import RequestClassroom
from service.classroomService import ClassroomService
from typing import Annotated
from fastapi import status
from sqlalchemy.orm.exc import NoResultFound
from service.tokenHandler import TokenHandler
from model.role import Role
from model.user import User
from service.userService import get_current_user

router = APIRouter()


        
dependency = Annotated[ClassroomService,Depends()] 
user_dependency = Annotated[User,Depends(get_current_user)]


# get all classrooms end point
@router.get("/")
@TokenHandler.role_required([Role.ADMIN,Role.STUDENT,Role.TEACHER])
async def get_all(user: user_dependency,classroom_service: dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authentication failed")
    _classrooms = classroom_service.get_classrooms()
    return _classrooms
     
 
    
# get classroom by id end point
@router.get("/{classroom_id}")
@TokenHandler.role_required([Role.ADMIN,Role.STUDENT,Role.TEACHER])
async def get(user:user_dependency,classroom_id: int, classroom_service: dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authentication failed")
    try:
        _classroom = classroom_service.get_classroom_by_id(classroom_id=classroom_id)
        return _classroom
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    
    
# create classroom end point
@router.post("/create")
@TokenHandler.role_required([Role.ADMIN])
async def create(user:user_dependency,classr: RequestClassroom, classroom_service: dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authentication failed")
    _classroom = classroom_service.create_classroom(classroom=classr)
    return _classroom
   
    
# delete classroom end point
@router.delete("/delete/{classroom_id}")
@TokenHandler.role_required([Role.ADMIN])
async def delete(user:user_dependency,classroom_id: int , classroom_service: dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authentication failed")
    try:
        _classroom = classroom_service.delete_classroom(classroom_id=classroom_id)
        return _classroom
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
        
        
# update classroom end point
@router.patch("/update/{classroom_id}")
@TokenHandler.role_required([Role.ADMIN])
async def update(user:user_dependency,classroom_id: int, classr: RequestClassroom, classroom_service: dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authentication failed")
    try:
        _classroom = classroom_service.update_classroom(
            classroom_id=classroom_id,
            name=classr.name
            )
        return _classroom
    except:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Fail to update data")