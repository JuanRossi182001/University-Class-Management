from sqlalchemy.orm import Session
from schema.carrerSchema import CarrerSchema
from model.carrer import Carrer
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
# get all carrers
def get_carrers(db:Session) -> list:
    return db.query(Carrer).all()


# get carrer by id
def get_carrer_by_id(db:Session, carrer_id:int) -> Carrer:
    try:
        return db.query(Carrer).filter(Carrer.id == carrer_id).first()
    except:
        raise HTTPException(status_code=404,detail="Error, Carrer not found")
    
    
# create a new carrer
def create_carrer(db:Session, carrer: CarrerSchema) -> CarrerSchema:
    try:
        _carrer = Carrer(name=carrer.name,duration_in_years = carrer.duration_in_years)
        db.add(_carrer)
        db.commit()
        db.refresh(_carrer)
        return CarrerSchema.from_orm(_carrer)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Unprocessable Entity: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
     
    
    


# delete carrer
def delete_carrer(db:Session, carrer_id: int) -> str:
    try:
        _carrer = get_carrer_by_id(db=db,carrer_id=carrer_id)
        db.delete(_carrer)
        db.commit()
        return f"Carrer {carrer_id} successfully deleted"
    except:
        raise HTTPException(status_code=404,detail="Error, Carrer not found")
    
    
# update carrer
def update_carrer(db:Session, carrer_id: int, name: str,duration_in_years: int) -> CarrerSchema:
    try:
        _carrer = get_carrer_by_id(db=db,carrer_id=carrer_id)
        _carrer.name = name
        _carrer.duration_in_years = duration_in_years
        db.commit()
        db.refresh(_carrer)
        return CarrerSchema.from_orm(_carrer)
    except:
        raise HTTPException(status_code=422,detail="Unprocessable Entity")