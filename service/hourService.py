from sqlalchemy.orm import Session
from model.hour import  Hour
from schema.hourSchema import HourSchema
from fastapi import HTTPException
from datetime import datetime
from sqlalchemy import and_
from typing import Annotated
from fastapi.param_functions import Depends
from config.db.connection import get_db
from sqlalchemy.orm.exc import NoResultFound


class HourService():
    
    def __init__(self, db: Annotated[Session,Depends(get_db)]) -> None:
        self.db = db

    # get all hours
    def get_hours(self) -> list:
        return self.db.query(Hour).all()

    # get hour by id
    def get_hour_by_id(self, hour_id: int) -> Hour:
        _hour = self.db.query(Hour).filter(Hour.id == hour_id).first()
        if not _hour:
            raise NoResultFound(f"Error, hour {hour_id} not found")
        return _hour
        
        
    # create hour
    def create_hour(self, hour: HourSchema) -> HourSchema:
            if self.comprobation(hour=hour):
                raise HTTPException(status_code=422, detail="Error, The schedule overlaps with another schedule in the same classroom.")
            
            _hour = Hour(**hour.model_dump())
            self.db.add(_hour)
            self.db.commit()
            self.db.refresh(_hour)
            return HourSchema.model_validate(_hour)
        
        
        
        
    # delete hour
    def delete_hour(self, hour_id: int) -> str:
        _hour = self.get_hour_by_id(hour_id=hour_id)
        self.db.delete(_hour)
        self.db.commit()
        return f"Hour {hour_id} successfully deleted"
           
        
        
    # update hour
    def update_hour(self,hour_id:int,start_hour:datetime,end_hour:datetime,
                    subject_id:int,classroom_id:int) -> HourSchema:
        
            _hour = self.get_hour_by_id(hour_id=hour_id)
            
            # temporal schema for comprobation
            temp_hour = HourSchema(
                start_hour=start_hour,
                end_hour=end_hour,
                subject_id=subject_id,
                classroom_id=classroom_id
            )
            if self.comprobation(hour=temp_hour, exclude_hour_id=hour_id):
                raise HTTPException(status_code=422, detail="Error, The schedule overlaps with another schedule in the same classroom.")
            
            _hour.start_hour = start_hour
            _hour.end_hour = end_hour
            _hour.subject_id = subject_id
            _hour.classroom_id = classroom_id
            self.db.commit()
            self.db.refresh(_hour)
            return HourSchema.model_validate(_hour)
       
            
            
            
            
    # hour overlap comprobation 
    def is_time_overlap(start_time1:datetime,end_time1:datetime,start_time2:datetime,end_time2:datetime) -> bool:
        return start_time1 <= end_time2 and start_time2 <= end_time1



    # Check to see if there are any existing classroom schedules during the same time period.
    def comprobation(self, hour: HourSchema, exclude_hour_id: int = None) -> bool:
        query = self.db.query(Hour).filter(
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