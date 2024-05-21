from fastapi import APIRouter, HTTPException,Depends
from schema.classroomSchema import RequestClassroom,Response
from service.classroomService import create_classroom,delete_classroom,update_classroom,get_classroom_by_id,get_classrooms
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


# get all classrooms end point
@router.get("/classrooms")
async def get_all_classrooms(db: db_dependency):
    try:
        _classrooms = get_classrooms(db=db)
        return Response(code="200", status="OK",message="Succes fetch all data", result=_classrooms).dict(exclude_none=True)
    except:
        raise HTTPException(status_code=400,detail="Fail to get data")
 
    
# get classroom by id end point
@router.get("/classrooms/{classroom_id}")
async def get_by_id(classroom_id: int, db: db_dependency):
    try:
        _classroom = get_classroom_by_id(classroom_id=classroom_id,db=db)
        return Response(code="200", status="OK",message="Succes fetch all data", result=_classroom).dict(exclude_none=True)
    except:
        raise HTTPException(status_code=400,detail="Fail to get data")
    
    
# create classroom end point
@router.post("/classrooms/create")
async def create(classr: RequestClassroom, db: db_dependency):
    try:
        create_classroom(db=db,classroom=classr.parameter)
        return Response(code="200", status="OK",message="Classroom created Successfully", result=None).dict(exclude_none=True)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail="Fail to create data")
  
    
# delete classroom end point
@router.delete("/classrooms/delete/{classroom_id}")
async def delete(classroom_id: int ,db: db_dependency):
    try:
        delete_classroom(db=db,classroom_id=classroom_id)
        return Response(code="200", status="OK",message="Success delete data", result={}).dict(exclude_none=True)
    except:
        raise HTTPException(status_code=500,detail="Fail to delete data")
        
        
# update classroom end point
@router.patch("/classrooms/update/{classroom_id}")
async def update(classroom_id: int, classr: RequestClassroom, db: db_dependency):
    try:
        _classroom = update_classroom(db=db,classroom_id=classroom_id,name=classr.parameter.name)
        return Response(code="200",status="OK",message ="Succes update data", result =_classroom).dict(exclude_none = True)
    except:
        raise HTTPException(status_code=500,detail="Fail to update data")