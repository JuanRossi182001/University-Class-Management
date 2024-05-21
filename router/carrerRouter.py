from fastapi import APIRouter, HTTPException,Depends
from schema.carrerSchema import RequestCarrer,Response
from service.carrerService import create_carrer,delete_carrer,update_carrer,get_carrer_by_id,get_carrers
from config.config import sessionlocal
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter()


def get_db():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session,Depends(get_db)]


# get all carrers end point
@router.get("/carrers")
async def get_all_carrers(db:db_dependency):
    try:
        _carrers = get_carrers(db=db)
        return Response(code="200", status="OK",message="Succes fetch all data", result=_carrers).dict(exclude_none=True)
    except:
        raise HTTPException(status_code=400,detail="Fail to get data")
    
    
# get carrer by id end point
@router.get("/carrers/{carrer_id}")
async def get_by_id(carrer_id: int, db: db_dependency):
    try:
        _carrer = get_carrer_by_id(db=db,carrer_id=carrer_id)
        return Response(code="200", status="OK",message="Succes fetch all data", result=_carrer).dict(exclude_none=True)
    except:
        raise HTTPException(status_code=400,detail="Fail to get data") 
    
    
# create carrer end point
@router.post("/carrers/create")
async def create(carr: RequestCarrer, db: db_dependency):
    try:
        create_carrer(db=db,carrer=carr.parameter)
        return Response(code="200", status="OK",message="Carrer created Successfully", result=None).dict(exclude_none=True)
    except:
        raise HTTPException(status_code=500,detail="Fail to create data")
    
# delete carrer end point
@router.delete("/carrers/delete/{carrer_id}")
async def delete(carrer_id: int, db: db_dependency):
    try:
        delete_carrer(db=db,carrer_id=carrer_id)
        return Response(code="200", status="OK",message="Success delete data", result={}).dict(exclude_none=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create data: {str(e)}")
        
    

# update carrer end point
@router.patch("/carrers/update/{carrer_id}")
async def update(carrer_id: int, carr: RequestCarrer, db: db_dependency):
    try:
        _carrer = update_carrer(db=db,carrer_id=carrer_id,name=carr.parameter.name,
                                duration_in_years=carr.parameter.duration_in_years)
        return Response(code="200",status="OK",message ="Succes update data", result =_carrer).dict(exclude_none = True)
    except:
        raise HTTPException(status_code=500,detail="Fail to update data")
