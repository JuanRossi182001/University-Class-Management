from sqlalchemy.orm import Session
from schema.classroomSchema import ClassroomSchema
from model.classroom import Classroom
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError


# get all classrooms
def get_classrooms(db:Session) -> list:
    return db.query(Classroom).all()


# get classroom by id
def get_classroom_by_id(db:Session, classroom_id:int) -> Classroom:
    try:
        return db.query(Classroom).filter(Classroom.id == classroom_id).first()
    except:
        raise HTTPException(status_code=404,detail="Error, Classroom not found")
    
    
# create a new classroom
def create_classroom(db:Session, classroom: ClassroomSchema) -> ClassroomSchema:
    try:
        _classroom = Classroom(name=classroom.name)
        db.add(_classroom)
        db.commit()
        db.refresh(_classroom)
        return ClassroomSchema.from_orm(_classroom)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Unprocessable Entity: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
        


# delete classroom
def delete_classroom(db:Session, classroom_id: int) -> str:
    try:
        _classroom = get_classroom_by_id(db=db,classroom_id=classroom_id)
        db.delete(_classroom)
        db.commit()
        return f"Classroom {classroom_id} successfully deleted"
    except:
        raise HTTPException(status_code=404,detail="Error, Classroom not found")
    
    
# update Classroom
def update_classroom(db:Session, classroom_id: int, name: str) -> ClassroomSchema:
    try:
        _classroom = get_classroom_by_id(db=db,classroom_id=classroom_id)
        _classroom.name = name
        db.commit()
        db.refresh(_classroom)
        return ClassroomSchema.from_orm(_classroom)
    except:
        raise HTTPException(status_code=422,detail="Unprocessable Entity")