from pydantic import BaseModel,Field
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
        

class RequestSubject(BaseModel):
    parameter: SubjectSchema = Field(...)
    
    
class Response(GenericModel,Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]