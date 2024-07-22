from fastapi import APIRouter, HTTPException,Depends
from schema.hourSchema import RequestHour
from service.hourService import HourService
from typing import Annotated
from fastapi import status
from sqlalchemy.orm.exc import NoResultFound
from service.tokenHandler import TokenHandler
from model.role import Role
from model.user import User
from service.userService import get_current_user

router = APIRouter()


        
dependency = Annotated[HourService,Depends()]
user_dependency = Annotated[User,Depends(get_current_user)]

# get all hours end point
@router.get("/")
@TokenHandler.role_required([Role.ADMIN,Role.STUDENT,Role.TEACHER])
async def get_all(user:user_dependency,hour_service: dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authentication failed")
    _hours = hour_service.get_hours()
    return _hours
     
# get hour by id end point
@router.get("/{hour_id}")
@TokenHandler.role_required([Role.ADMIN,Role.STUDENT,Role.TEACHER])
async def get(user:user_dependency,hour_id: int,hour_service: dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authentication failed")
    try:
        _hour = hour_service.get_hour_by_id(hour_id=hour_id)
        return _hour
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    

# create hour end point
@router.post("/create")
@TokenHandler.role_required([Role.ADMIN,Role.TEACHER])
async def create(user:user_dependency,hour: RequestHour, hour_service: dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authentication failed")
    _hour = hour_service.create_hour(hour=hour)
    return _hour
      

# delete hour end point
@router.delete("/delete/{hour_id}")
@TokenHandler.role_required([Role.ADMIN,Role.TEACHER])
async def delete(user:user_dependency,hour_id: int, hour_service: dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authentication failed")
    try:
       _hour = hour_service.delete_hour(hour_id=hour_id)
       return _hour
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    

# update hour end point 
@router.patch("/update/{hour_id}")
@TokenHandler.role_required([Role.ADMIN,Role.TEACHER])
async def update(user:user_dependency,hour_id: int, hour: RequestHour, hour_service: dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authentication failed")
    try:
        _hour = hour_service.update_hour(
                            hour_id=hour_id,
                            start_hour=hour.start_hour,
                            end_hour=hour.end_hour,
                            subject_id=hour.subject_id,
                            classroom_id=hour.classroom_id
                            )
        return _hour
    except:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Fail to update data")
