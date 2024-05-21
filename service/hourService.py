from sqlalchemy.orm import Session
from model.hour import  Hour
from schema.hourSchema import HourSchema
from fastapi import HTTPException
from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

# get all hours
def get_hours(db:Session) -> list:
    return db.query(Hour).all()

# get hour by id
def get_hour_by_id(db:Session, hour_id: int) -> Hour:
    try:
        return db.query(Hour).filter(hour_id == Hour.id).first()
    except:
        raise HTTPException(status_code=404, detail="Error, Hour not found")
    
    
# create hour
def create_hour(db:Session, hour: HourSchema) -> HourSchema:
    try:
        if comprobation(db=db,hour=hour):
            raise HTTPException(status_code=422, detail="Error, The schedule overlaps with another schedule in the same classroom.")
        
        _hour = Hour(start_hour = hour.start_hour,end_hour = hour.end_hour,
                     subject_id = hour.subject_id,classroom_id = hour.classroom_id)
        db.add(_hour)
        db.commit()
        db.refresh(_hour)
        return HourSchema.from_orm(_hour)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Unprocessable Entity: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
        
    
    
    
# delete hour
def delete_hour(db:Session, hour_id: int) -> str:
    try:
        _hour = get_hour_by_id(db=db,hour_id=hour_id)
        db.delete(_hour)
        db.commit()
        return f"Hour {hour_id} successfully deleted"
    except:
        raise HTTPException(status_code=404,detail="Hour not found")
    
    
# update hour
def update_hour(db:Session,hour_id:int,start_hour:datetime,end_hour:datetime,
                subject_id:int,classroom_id:int) -> HourSchema:
    try:
        _hour = get_hour_by_id(db=db,hour_id=hour_id)
        
        # temporal schema for comprobation
        temp_hour = HourSchema(
            start_hour=start_hour,
            end_hour=end_hour,
            subject_id=subject_id,
            classroom_id=classroom_id
        )
        if comprobation(db=db, hour=temp_hour, exclude_hour_id=hour_id):
            raise HTTPException(status_code=422, detail="Error, The schedule overlaps with another schedule in the same classroom.")
        
        _hour.start_hour = start_hour
        _hour.end_hour = end_hour
        _hour.subject_id = subject_id
        _hour.classroom_id = classroom_id
        db.commit()
        db.refresh(_hour)
        return HourSchema.from_orm(_hour)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Unprocessable Entity: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
        
        
        
        
# hour overlap comprobation 
def is_time_overlap(start_time1:datetime,end_time1:datetime,start_time2:datetime,end_time2:datetime) -> bool:
    return start_time1 <= end_time2 and start_time2 <= end_time1



# Check to see if there are any existing classroom schedules during the same time period.
def comprobation(db: Session, hour: HourSchema, exclude_hour_id: int = None) -> bool:
    query = db.query(Hour).filter(
        and_(
            Hour.classroom_id == hour.classroom_id,
            Hour.start_hour < hour.end_hour,
            hour.start_hour < Hour.end_hour
        )
    )
    
    if exclude_hour_id:
        query = query.filter(Hour.id != exclude_hour_id)
    
    existing_hours = query.all()
    return bool(existing_hours)