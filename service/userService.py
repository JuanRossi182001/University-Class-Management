from typing import Annotated,List
from sqlalchemy.orm import Session
from fastapi.param_functions import Depends
from fastapi import HTTPException, status
from config.db.connection import get_db
from sqlalchemy.orm.exc import NoResultFound
from model.user import User 
from schema.userSchema import UserSchema , UserResponse
from passlib.context import CryptContext
from datetime import timedelta,datetime
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from typing import List


bcryptContext = CryptContext(schemes=['bcrypt'], deprecated ='auto')
SECRET_KEY = '4a4e0a14fb014a0abbbd4fb72c8dfd72'
ALGORITH = 'HS256'
oauth_bearer = OAuth2PasswordBearer(tokenUrl='user/token')

class UserService():
    def __init__(self, db: Annotated[Session,Depends(get_db)]) -> None:
        self.db = db
        
    # get all users
    def get_users(self) -> List[UserResponse]:
        user_list = self.db.query(User).all()
        return [UserResponse.model_validate(user) for user in user_list] # list comprhesion 
    
        
        
        
    # get user by id
    def get_user_by_id(self, user_id: int) -> User:
        _user = self.db.query(User).filter(User.id == user_id).first()
        if not _user:
            raise NoResultFound
        return UserResponse.model_validate(_user)
    
    def get_user_by_id_to_delete(self, user_id: int) -> User:
        _user = self.db.query(User).filter(User.id == user_id).first()
        if not _user:
            raise NoResultFound
        return _user
    
    # create user
    def create(self,user: UserSchema) -> UserResponse:
        hashed_password = bcryptContext.hash(user.password)
        _user = User(username = user.username,
                     password = hashed_password,
                     role_id = user.role_id)
        print(f"role_id received: {_user.role_id}")
        self.db.add(_user)
        self.db.commit()
        self.db.refresh(_user)
        return  UserResponse.model_validate(_user)
    
    # delete user
    def delete(self, user_id: int) -> str:
        _user = self.get_user_by_id_to_delete(user_id=user_id)
        self.db.delete(_user)
        self.db.commit()
        return f"User {user_id} successfully deleted"
    
    
    def authenticate_user(self,username: str,password: str) -> User :
        _user = self.db.query(User).filter(User.username == username).first()
        if not _user:
            return None
        if not bcryptContext.verify(password, _user.password):
            return None
        return  _user
    
    def create_acces_token(self, username: str, user_id: int,roles: List[int] , expires_delta: timedelta) -> str:
        to_encode = {'sub': username, 'id': user_id,'roles': roles }
        expire = datetime.utcnow() + expires_delta
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITH)
        return encoded_jwt
    
    
def get_current_user(user_service:Annotated[UserService,Depends()],token: Annotated[str,Depends(oauth_bearer)]) -> UserResponse:
        payload = jwt.decode(token,SECRET_KEY)
        user_id: int = payload.get('id')
        user = user_service.get_user_by_id(user_id=user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Could not validate user.")
        return UserResponse.model_validate(user)
    
   