from pydantic import BaseModel,Field
from typing import TypeVar,Optional,Generic
from pydantic.generics import GenericModel
from datetime import datetime

T = TypeVar('T')

class HourSchema(BaseModel):
    start_hour: Optional[datetime] = None
    end_hour: Optional[datetime] = None
    subject_id: Optional[int] = None
    classroom_id: Optional[int] = None
    
    class Config:
        orm_mode = True
        from_attributes = True
        
        
class RequestHour(HourSchema):
    pass
    

class Response(GenericModel,Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]
    
    