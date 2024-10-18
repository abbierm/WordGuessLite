from fastapi import FastAPI, Depends
from dependencies import get_cache
from routers import play
import uvicorn


app = FastAPI(dependencies=[Depends(get_cache)])
app.include_router(play.router)

@app.get("/")
async def root():
    return {"message": "hello this is the homepage"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)