from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Metro Reviews routes
@app.get("/claim")
async def claim():
    ...

@app.get("/unclaim")
async def unclaim():
    ...
    
@app.get("/approve")
async def approve():
    ...

@app.get("/deny")
async def deny():
    ...
