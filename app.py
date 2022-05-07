import json

# This contains the list specific code
import act

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

class Bot(BaseModel):
    bot_id: str
    reviewer: str
    username: str
    description: str
    long_description: str
    nsfw: bool
    tags: list[str]
    owner: str
    extra_owners: list[str]
    website: str | None = None
    github: str | None = None # May be added later
    support: str | None = None
    donate: str | None = None
    library: str | None = None
    prefix: str | None = None

# Metro Reviews routes
@app.get("/claim")
async def claim(bot: Bot, auth: str = Depends(auth_header)):
    if (auth := await _auth(auth)):
        return auth 
    
    return (await act.claim(app, bot)) or {}

@app.get("/unclaim")
async def unclaim(bot: Bot, auth: str = Depends(auth_header)):
    if (auth := await _auth(auth)):
        return auth 
    
    return (await act.unclaim(app, bot)) or {}

    
@app.get("/approve")
async def approve(bot: Bot, auth: str = Depends(auth_header)):
    if (auth := await _auth(auth)):
        return auth 

    return (await act.approve(app, bot)) or {}

@app.get("/deny")
async def deny(bot: Bot, auth: str = Depends(auth_header)):
    if (auth := await _auth(auth)):
        return auth 
    
    return (await act.deny(app, bot)) or {}

@app.on_event("startup")
async def prepare():
    await act.prepare(app)
