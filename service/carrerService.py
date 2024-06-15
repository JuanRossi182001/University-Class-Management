from sqlalchemy.orm import Session
from schema.carrerSchema import CarrerSchema
from model.carrer import Carrer
from typing import Annotated
from fastapi.param_functions import Depends
from config.db.connection import get_db
from sqlalchemy.orm.exc import NoResultFound

class CarrerService:
    
    def __init__(self, db: Annotated[Session,Depends(get_db)]) -> None:
        self.db = db
    
    # get all carrers
    def get_carrers(self) -> list:
        return self.db.query(Carrer).all()


    # get carrer by id
    def get_carrer_by_id(self, carrer_id: int) -> Carrer:
        _carrer = self.db.query(Carrer).filter(Carrer.id == carrer_id).first()
        if not _carrer:
            raise NoResultFound(f"Error, Carrer {carrer_id} not found")
        return _carrer
        
        
    # create a new carrer
    def create_carrer(self, carrer: CarrerSchema) -> CarrerSchema:
            _carrer = Carrer(**carrer.model_dump())
            self.db.add(_carrer)
            self.db.commit()
            self.db.refresh(_carrer)
            return CarrerSchema.model_validate(_carrer)
        
        
    # delete carrer
    def delete_carrer(self, carrer_id: int) -> str:
        _carrer = self.get_carrer_by_id(carrer_id=carrer_id)
        self.db.delete(_carrer)
        self.db.commit()
        return f"Carrer {carrer_id} successfully deleted"
        
        
    # update carrer
    def update_carrer(self, carrer_id: int, name: str,duration_in_years: int) -> CarrerSchema:
        _carrer = self.get_carrer_by_id(carrer_id=carrer_id)
        _carrer.name = name
        _carrer.duration_in_years = duration_in_years
        self.db.commit()
        self.db.refresh(_carrer)
        return CarrerSchema.from_orm(_carrer)
        