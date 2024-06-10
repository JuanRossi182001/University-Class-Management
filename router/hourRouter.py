from fastapi import APIRouter, HTTPException,Depends
from schema.hourSchema import RequestHour, Response
from service.hourService import HourService
from config.config import sessionlocal
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import status
from sqlalchemy.orm.exc import NoResultFound

router = APIRouter()


        
dependency = Annotated[HourService,Depends()]

# get all hours end point
@router.get("/")
async def get_all(hour_service: dependency):
    _hours = hour_service.get_hours()
    return _hours
     
# get hour by id end point
@router.get("/{hour_id}")
async def get(hour_id: int,hour_service: dependency ):
    try:
        _hour = hour_service.get_hour_by_id(hour_id=hour_id)
        return _hour
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    

# create hour end point
@router.post("/create")
async def create(hour: RequestHour, hour_service: dependency):
    _hour = hour_service.create_hour(hour=hour)
    return _hour
      

# delete hour end point
@router.delete("/delete/{hour_id}")
async def delete(hour_id: int, hour_service: dependency):
    try:
       _hour = hour_service.delete_hour(hour_id=hour_id)
       return _hour
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    

# update hour end point 
@router.patch("/update/{hour_id}")
async def update(hour_id: int, hour: RequestHour, hour_service: dependency):
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
