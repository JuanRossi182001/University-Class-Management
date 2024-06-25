from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    
    class Config:
        from_attributes = True
        
        
  
class RequestUser(UserSchema):
    pass