from fastapi import FastAPI
from router import carrerRouter,classroomRouter,hourRouter,subjectRouter



app = FastAPI()
app.include_router(carrerRouter.router)
app.include_router(classroomRouter.router)
app.include_router(hourRouter.router)
app.include_router(subjectRouter.router)



@app.get("/")
async def hello():
    return "Hello Mother Fucker"
