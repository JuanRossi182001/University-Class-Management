from pydantic import BaseModel,Field
from typing import TypeVar,Optional,Generic
from pydantic.generics import GenericModel


T = TypeVar('T')

class ClassroomSchema(BaseModel):
    name: Optional[str] = None
    
    class Config:
        orm_mode = True
        from_attributes = True
        
        
class RequestClassroom(BaseModel):
    parameter: ClassroomSchema = Field(...)
    
    
    
class Response(GenericModel,Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]
    