import json

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel

app = FastAPI()

with open("secrets.json") as secrets:
    secrets = json.load(secrets)

async def _auth(key: str) -> ORJSONResponse | None:
    if key != secrets["secret_key"]:
        return ORJSONResponse({"detail": "Invalid secret key"}, status_code=401)

auth_header = APIKeyHeader(name='Authorization')
    
# Metro Reviews routes
@app.get("/claim")
async def claim(auth: str = Depends(auth_header)):
    if (auth := await _auth(auth)):
        return auth 

@app.get("/unclaim")
async def unclaim(auth: str = Depends(auth_header)):
    if (auth := await _auth(auth)):
        return auth 

    
@app.get("/approve")
async def approve(auth: str = Depends(auth_header)):
    if (auth := await _auth(auth)):
        return auth 


@app.get("/deny")
async def deny(auth: str = Depends(auth_header)):
    if (auth := await _auth(auth)):
        return auth 

