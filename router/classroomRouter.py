from fastapi import APIRouter, HTTPException,Depends
from schema.classroomSchema import RequestClassroom,Response
from service.classroomService import ClassroomService
from typing import Annotated
from fastapi import status
from sqlalchemy.orm.exc import NoResultFound

router = APIRouter()


        
dependency = Annotated[ClassroomService,Depends()]      


# get all classrooms end point
@router.get("/")
async def get_all(classroom_service: dependency):
    _classrooms = classroom_service.get_classrooms()
    return _classrooms
     
 
    
# get classroom by id end point
@router.get("/{classroom_id}")
async def get(classroom_id: int, classroom_service: dependency):
    try:
        _classroom = classroom_service.get_classroom_by_id(classroom_id=classroom_id)
        return _classroom
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    
    
# create classroom end point
@router.post("/create")
async def create(classr: RequestClassroom, classroom_service: dependency):
    _classroom = classroom_service.create_classroom(classroom=classr)
    return _classroom
   
    
# delete classroom end point
@router.delete("/delete/{classroom_id}")
async def delete(classroom_id: int , classroom_service: dependency):
    try:
        _classroom = classroom_service.delete_classroom(classroom_id=classroom_id)
        return _classroom
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
        
        
# update classroom end point
@router.patch("/update/{classroom_id}")
async def update(classroom_id: int, classr: RequestClassroom, classroom_service: dependency):
    try:
        _classroom = classroom_service.update_classroom(
            classroom_id=classroom_id,
            name=classr.name
            )
        return _classroom
    except:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Fail to update data")