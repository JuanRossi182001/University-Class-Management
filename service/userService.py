from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.param_functions import Depends
from fastapi import HTTPException, status
from config.db.connection import get_db
from sqlalchemy.orm.exc import NoResultFound
from model.user import User
from schema.userSchema import UserSchema
from passlib.context import CryptContext
from datetime import timedelta,datetime
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer


bcryptContext = CryptContext(schemes=['bcrypt'], deprecated ='auto')
SECRET_KEY = '4a4e0a14fb014a0abbbd4fb72c8dfd72'
ALGORITH = 'HS256'
oauth_bearer = OAuth2PasswordBearer(tokenUrl='user/token')

class UserService():
    def __init__(self, db: Annotated[Session,Depends(get_db)]) -> None:
        self.db = db
        
    # get all users
    def get_users(self):
        return self.db.query(User).all()
    
        
        
        
    # get user by id
    def get_user_by_id(self, user_id: int):
        _user = self.db.query(User).filter(User.id == user_id).first()
        if not _user:
            raise NoResultFound
        return _user
    
    # create user
    def create(self,user: UserSchema):
        hashed_password = bcryptContext.hash(user.password)
        _user = User(username = user.username,
                     password = hashed_password)
        self.db.add(_user)
        self.db.commit()
        self.db.refresh(_user)
        return _user
    
    # delete user
    def delete(self, user_id: int) -> str:
        _user = self.get_user_by_id(user_id=user_id)
        self.db.delete(_user)
        self.db.commit()
        return f"User {user_id} successfully deleted"
    
    def authenticate_user(self,username: str,password: str):
        _user = self.db.query(User).filter(User.username == username).first()
        if not _user:
            return None
        if not bcryptContext.verify(password, _user.password):
            return None
        return _user
    
    def create_acces_token(self, username: str, user_id: int, expires_delta: timedelta):
        to_encode = {'sub': username, 'id': user_id}
        expire = datetime.utcnow() + expires_delta
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITH)
        return encoded_jwt
    """ encode = {'sub': username,'id': user_id}
        expires = datetime.utcnow() + expires_delta
        encode.update({'exp':expires})
        return jwt.encode(encode,SECRET_KEY, algorithm=ALGORITH)
        """
    async def get_current_user(token: Annotated[str,Depends(oauth_bearer)]):
        payload = jwt.decode(token,SECRET_KEY)
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Could not validate user.")
        return {'username': username, 'id': user_id}