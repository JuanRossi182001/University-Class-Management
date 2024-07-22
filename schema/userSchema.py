from pydantic import BaseModel
from typing import Optional
from typing import List


class UserSchema(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[List[int]] = None  #TODO: SACAR LOS OPTIONAL # aca colocar tmb lista de roles 
    
    class Config:
        from_attributes = True
        
        
        
class UserResponse(BaseModel):
    id: int
    username: Optional[str] = None
    role_id: Optional[List[int]] = None
    
    class Config:
        from_attributes = True
  
class RequestUser(UserSchema):
    pass