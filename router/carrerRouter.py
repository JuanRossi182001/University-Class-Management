from fastapi import APIRouter, HTTPException, Depends
from schema.carrerSchema import RequestCarrer
from service.carrerService import CarrerService
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import status
from sqlalchemy.orm.exc import NoResultFound

router = APIRouter()



dependency = Annotated[CarrerService,Depends()]


# get all carrers end point
@router.get("/")
async def get_all(carrer_service: dependency):
    _carrers = carrer_service.get_carrers()
    return _carrers
    
    
    
# get carrer by id end point
@router.get("/{carrer_id}")
async def get(carrer_id: int, carrer_servie: dependency):
    try:
        _carrer = carrer_servie.get_carrer_by_id(carrer_id=carrer_id)
        return _carrer
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

        
    
    
# create carrer end point
@router.post("/create")
async def create(carr: RequestCarrer, carrer_service: dependency):
    _carrer = carrer_service.create_carrer(carrer=carr)
    return _carrer
     
        
    
# delete carrer end point
@router.delete("/delete/{carrer_id}")
async def delete(carrer_id: int, carrer_service: dependency):
    try:
        _carrer = carrer_service.delete_carrer(carrer_id=carrer_id)
        return _carrer
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={str(e)})
        
    

# update carrer end point
@router.patch("/update/{carrer_id}")
async def update(carrer_id: int, carr: RequestCarrer, carrer_service: dependency):
    try:
        _carrer = carrer_service.update_carrer(
            carrer_id=carrer_id,
            name=carr.name,
            duration_in_years=carr.duration_in_years
            )
        return _carrer
    except:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Fail to update data")
