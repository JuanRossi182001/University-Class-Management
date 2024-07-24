from pydantic import BaseModel
from typing import TypeVar,Optional,Generic
from pydantic.generics import GenericModel

T = TypeVar('T')

class SubjectSchema(BaseModel):
    name: Optional[str] = None
    semester: Optional[str] = None
    carrer_id: Optional[int] = None
    
    class Config:
        orm_mode = True
        from_attributes = True
        
        
class SubjectResponse(BaseModel):
    name: Optional[str] = None
    semester: Optional[str] = None
    carrer_id: Optional[int] = None
    
    class Config:
        orm_mode = True
        from_attributes = True
        

class RequestSubject(SubjectSchema):
    pass
    
    
class Response(GenericModel,Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]