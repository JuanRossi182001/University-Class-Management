from fastapi import FastAPI
from router import carrerRouter, classroomRouter, hourRouter, subjectRouter


app = FastAPI()
app.include_router(carrerRouter.router, prefix="/carrer", tags=["carer"])
app.include_router(classroomRouter.router, prefix="/classroom", tags=["classroom"])
app.include_router(
    hourRouter.router,
)
app.include_router(subjectRouter.router, tags=["subjects"])


@app.get("/")
async def hello():
    return "Hello Mother Fucker"
