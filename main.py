from fastapi import FastAPI
from router import carrerRouter,classroomRouter,hourRouter,subjectRouter,userRouter




app = FastAPI()
app.include_router(carrerRouter.router, prefix="/carrer", tags=["carrer"])
app.include_router(classroomRouter.router, prefix="/classroom", tags=["classroom"])
app.include_router(hourRouter.router, prefix="/hour", tags=["hour"])
app.include_router(subjectRouter.router, prefix="/subject", tags=["subject"])
app.include_router(userRouter.router, prefix="/user", tags=["user"])

  

@app.get("/")
async def hello():
    return "Hello Sir"
