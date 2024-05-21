from fastapi import APIRouter, HTTPException,Depends
from schema.subjectSchema import RequestSubject,Response
from service.subjectService import create_subject,delete_subject,update_subject,get_subject_by_id,get_subjects
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
        
        
# get all subjects end point
@router.get("/subjects")
async def get_all_subjects(db: db_dependency):
    try:
        _subjects = get_subjects(db=db)
        return Response(code="200", status="OK",message="Succes fetch all data", result=_subjects).dict(exclude_none=True)
    except:
        raise HTTPException(status_code=400,detail="Fail to get data")
    
    
# get subject by id end point 
@router.get("/subjects/{subject_id}")
async def get_by_id(subject_id: int,db: db_dependency):
    try:
        _subject = get_subject_by_id(subject_id=subject_id,db=db)
        return Response(code="200", status="OK",message="Succes fetch all data", result=_subject).dict(exclude_none=True)
    except:
        raise HTTPException(status_code=400,detail="Fail to get data")
    

# create subject end point
@router.post("/subjects/create")
async def create(sub: RequestSubject, db: db_dependency):
    try:
        create_subject(db=db,subject=sub.parameter)
        return Response(code="200", status="OK",message="Subject created Successfully", result=None).dict(exclude_none=True)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail="Fail to create data")
    

# delete subject end point
@router.delete("/subjects/delete/{subject_id}")
async def delete(subject_id: int, db: db_dependency):
    try:
        delete_subject(db=db,subject_id=subject_id)
        return Response(code="200", status="OK",message="Success delete data", result={}).dict(exclude_none=True)
    except:
        raise HTTPException(status_code=500,detail="Fail to delete data")
    
 
# update subject end point   
@router.patch("/subjects/update/{subject_id}")
async def update(subject_id: int, sub: RequestSubject , db: db_dependency):
    try:
        _subject = update_subject(db=db,subject_id=subject_id,name=sub.parameter.name,
                       semester=sub.parameter.semester,carrer_id=sub.parameter.carrer_id)
        return Response(code="200",status="OK",message ="Succes update data", result =_subject).dict(exclude_none = True)
    except:
        raise HTTPException(status_code=500,detail="Fail to update data")