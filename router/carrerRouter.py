from fastapi import APIRouter, HTTPException, Depends
from schema.carrerSchema import RequestCarrer
from service.carrerService import CarrerService
from typing import Annotated
from fastapi import status
from sqlalchemy.orm.exc import NoResultFound
from service.tokenHandler import TokenHandler
from model.role import Role
from model.user import User
from service.userService import get_current_user
router = APIRouter()



dependency = Annotated[CarrerService,Depends()]
user_dependency = Annotated[User,Depends(get_current_user)]

# get all carrers end point
@router.get("/")
@TokenHandler.role_required([Role.ADMIN])
async def get_all(user: user_dependency,carrer_service: dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authentication failed")
    _carrers = carrer_service.get_carrers()
    return _carrers
    
    
    
# get carrer by id end point
@router.get("/{carrer_id}")
@TokenHandler.role_required([Role.ADMIN])
async def get(user: user_dependency,carrer_id: int, carrer_servie: dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authentication failed")
    try:
        _carrer = carrer_servie.get_carrer_by_id(carrer_id=carrer_id)
        return _carrer
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

        
    
    
# create carrer end point
@router.post("/create")
@TokenHandler.role_required([Role.ADMIN])
async def create(user: user_dependency,carr: RequestCarrer, carrer_service: dependency):
     if user is None:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authentication failed")
     _carrer = carrer_service.create_carrer(carrer=carr)
     return _carrer
     
        
    
# delete carrer end point
@router.delete("/delete/{carrer_id}")
@TokenHandler.role_required([Role.ADMIN])
async def delete(user: user_dependency,carrer_id: int, carrer_service: dependency):
    if user is None:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authentication failed")
    try:
        _carrer = carrer_service.delete_carrer(carrer_id=carrer_id)
        return _carrer
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={str(e)})
        
    

# update carrer end point
@router.patch("/update/{carrer_id}")
@TokenHandler.role_required([Role.ADMIN])
async def update(user:user_dependency,carrer_id: int, carr: RequestCarrer, carrer_service: dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authentication failed")
    try:
        _carrer = carrer_service.update_carrer(
            carrer_id=carrer_id,
            name=carr.name,
            duration_in_years=carr.duration_in_years
            )
        return _carrer
    except:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Fail to update data")
