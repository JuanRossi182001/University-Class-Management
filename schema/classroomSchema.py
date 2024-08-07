from pydantic import BaseModel
from typing import TypeVar,Optional,Generic
from pydantic.generics import GenericModel


T = TypeVar('T')

class ClassroomSchema(BaseModel):
    name: Optional[str] = None
    
    class Config:
        orm_mode = True
        from_attributes = True
        
        
class ClassroomResponse(BaseModel):
    name: Optional[str] = None
    
    class Config:
        orm_mode = True
        from_attributes = True
        
        
class RequestClassroom(ClassroomSchema):
    pass
    
    
    
class Response(GenericModel,Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]
    