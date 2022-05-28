import json

# This contains the list specific code
import act

from fastapi import FastAPI, Depends
from fastapi.responses import ORJSONResponse
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from typing import List

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
    tags: List[str]
    owner: str
    reason: str | None = "STUB_REASON"
    extra_owners: list[str]
    website: str | None = None
    github: str | None = None # May be added later
    support: str | None = None
    donate: str | None = None
    library: str | None = None
    prefix: str | None = None
    invite: str | None = None
    cross_add: bool | None = None

# Metro Reviews routes
@app.post("/claim")
async def claim(bot: Bot, auth: str = Depends(auth_header)):
    if (auth := await _auth(auth)):
        return auth 
    
    return (await act.claim(app, bot, secrets)) or {}

@app.post("/unclaim")
async def unclaim(bot: Bot, auth: str = Depends(auth_header)):
    if (auth := await _auth(auth)):
        return auth 
    
    return (await act.unclaim(app, bot, secrets)) or {}

    
@app.post("/approve")
async def approve(bot: Bot, auth: str = Depends(auth_header)):
    if (auth := await _auth(auth)):
        return auth 

    return (await act.approve(app, bot, secrets)) or {}

@app.post("/deny")
async def deny(bot: Bot, auth: str = Depends(auth_header)):
    if (auth := await _auth(auth)):
        return auth 
    
    return (await act.deny(app, bot, secrets)) or {}

@app.on_event("startup")
async def prepare():
    await act.prepare(app)
