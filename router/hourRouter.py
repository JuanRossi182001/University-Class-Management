from fastapi import APIRouter, HTTPException,Depends
from schema.hourSchema import RequestHour, Response
from service.hourService import create_hour,delete_hour,update_hour,get_hour_by_id,get_hours
from config.config import sessionlocal
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter()


def get_db():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session,Depends(get_db)]

# get all hours end point
@router.get("/hours")
async def get_all_hours(db: db_dependency):
    try:
        _hours = get_hours(db=db)
        return Response(code="200", status="OK",message="Succes fetch all data", result=_hours).dict(exclude_none=True)
    except:
        raise HTTPException(status_code=400,detail="Fail to get data")
    
    
# get hour by id end point
@router.get("/hours/{hour_id}")
async def get_by_id(hour_id: int, db: db_dependency):
    try:
        _hour = get_hour_by_id(db=db,hour_id=hour_id)
        return Response(code="200", status="OK",message="Succes fetch all data", result=_hour).dict(exclude_none=True)
    except:
        raise HTTPException(status_code=400,detail="Fail to get data")
    

# create hour end point
@router.post("/hours/create")
async def create(hour: RequestHour, db: db_dependency):
    try:
        create_hour(db=db,hour=hour.parameter)
        return Response(code="200", status="OK",message="Hour created Successfully", result=None).dict(exclude_none=True)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail="Fail to create data")
    

# delete hour end point
@router.delete("/hours/delete/{hour_id}")
async def delete(hour_id: int, db: db_dependency):
    try:
        delete_hour(db=db,hour_id=hour_id)
        return Response(code="200", status="OK",message="Success delete data", result={}).dict(exclude_none=True)
    except:
        raise HTTPException(status_code=500,detail="Fail to delete data")
    

# update hour end point 
@router.patch("/hours/update/{hour_id}")
async def update(hour_id: int, hour: RequestHour, db: db_dependency):
    try:
        _hour = update_hour(db=db,hour_id=hour_id,start_hour=hour.parameter.start_hour,
                            end_hour=hour.parameter.end_hour,subject_id=hour.parameter.subject_id,
                            classroom_id=hour.parameter.classroom_id)
        return Response(code="200",status="OK",message ="Succes update data", result =_hour).dict(exclude_none = True)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail="Fail to update data")
