from fastapi import APIRouter,HTTPException,status
from service.userService import UserService
from typing import Annotated
from fastapi import Depends, status
from schema.userSchema import RequestUser
from sqlalchemy.orm.exc import NoResultFound
from model.token import Token
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

router = APIRouter()


dependency = Annotated[UserService,Depends()]

@router.get("/")
async def get_all(user_service: dependency) :
    _users = user_service.get_users()
    return _users

@router.get("/{user_id}")
async def get(user_id: int, user_servie:dependency):
    try:
        _user = user_servie.get_user_by_id(user_id=user_id)
        return _user
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/create")
async def create(user_service: dependency,user: RequestUser):
    _user = user_service.create(user=user)
    return _user


@router.delete("/delete")
async def delete(user_id: int, user_service: dependency):
    try:
        _user = user_service.delete(user_id=user_id)
        return _user
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    
@router.post("/token", response_model=Token)
async def login_for_acces_token(form_data: OAuth2PasswordRequestForm = Depends(), user_service: UserService = Depends()):
    _user = user_service.authenticate_user(form_data.username, form_data.password)
    if not _user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    token = user_service.create_acces_token(_user.username, _user.id, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}
    
    
     