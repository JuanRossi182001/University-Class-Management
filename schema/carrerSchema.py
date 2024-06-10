from pydantic import BaseModel,Field
from typing import TypeVar,Optional,Generic
from pydantic.generics import GenericModel


T = TypeVar('T')

class CarrerSchema(BaseModel):
    name: Optional[str] = None
    duration_in_years: Optional[int] = None
    
    class Config:
        orm_mode = True
        from_attributes = True
        
        
class RequestCarrer(CarrerSchema):
    pass
    
    
    
class Response(GenericModel,Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]