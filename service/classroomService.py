from sqlalchemy.orm import Session
from schema.classroomSchema import ClassroomSchema
from model.classroom import Classroom
from typing import Annotated
from fastapi.param_functions import Depends
from router.db.connection import get_db
from sqlalchemy.orm.exc import NoResultFound


class ClassroomService():
    
    def __init__(self, db: Annotated[Session,Depends(get_db)]) -> None:
        self.db = db
    

    # get all classrooms
    def get_classrooms(self) -> list:
        return self.db.query(Classroom).all()


    # get classroom by id
    def get_classroom_by_id(self, classroom_id:int) -> Classroom:
        _classroom = self.db.query(Classroom).filter(Classroom.id == classroom_id).first()
        if not _classroom:
            raise NoResultFound(f"Error, classroom {classroom_id} not found")
        return _classroom
        
        
        
    # create a new classroom
    def create_classroom(self, classroom: ClassroomSchema) -> ClassroomSchema:
        _classroom = Classroom(**classroom.model_dump())
        self.db.add(_classroom)
        self.db.commit()
        self.db.refresh(_classroom)
        return ClassroomSchema.model_validate(_classroom)
        
            


    # delete classroom
    def delete_classroom(self, classroom_id: int) -> str:
        _classroom =self.get_classroom_by_id(classroom_id=classroom_id)
        self.db.delete(_classroom)
        self.db.commit()
        return f"Classroom {classroom_id} successfully deleted"
        
        
        
    # update Classroom
    def update_classroom(self, classroom_id: int, name: str) -> ClassroomSchema:
            _classroom = self.get_classroom_by_id(classroom_id=classroom_id)
            _classroom.name = name
            self.db.commit()
            self.db.refresh(_classroom)
            return ClassroomSchema.model_validate(_classroom)
        