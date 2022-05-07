# List specific code for IBL
#
# Replace this with code for your specific list

# Routes should be self-explanatory
import motor.motor_asyncio
import os
import secrets
import re
import datetime

async def prepare(app):
    """This sets up the mongodb database. It is a TODO"""
    # TODO: ask toxic if this is correct?
    app.mongo = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGO_URL"))[os.environ.get("MONGO_DBNAME")]

async def claim(app, bot):
    bot = await app.mongo.bots.find_one({"botID": bot.bot_id})
    if not bot:
        # We do not want to send any thing or do anything in claim/unclaim/deny if bot does not already exist
        return
    
    # Hopefully
    await app.mongo.bots.update_one({"botID": bot.bot_id}, {"$set": {"claimed": True, "claimedBy": bot.reviewer}})
    
    # TODO: ask toxic to make a proper claim embed

async def unclaim(app, bot):
    ...

async def approve(app, bot):
    bot = await app.mongo.bots.find_one({"botID": bot.bot_id})
    if not bot:
        # We need to insert a bot here
        await app.mongo.bots.insert_one({
            "botID": bot.bot_id,
            "botName": bot.username,
            "vanity": re.sub('[^a-zA-Z0-9]', '', bot.username).lower(),
            "note": "Metro-approved",
            "date": datetime.datetime.now(),
            "prefix": bot.prefix or "/",
            "website": bot.website or "None",
            "github": bot.github or "None",
            "donate": bot.donate or "None",
            "nsfw": bot.nsfw,
            "library": bot.library,
            "description": bot.description,
            "long_description": bot.long_description,
            "tags": ", ".join(bot.tags)
            "invite": bot.invite or f"https://discord.com/oauth2/authorize?client_id={bot.bot_id}&permissions=0&scope=bot%20applications.commands",
            "main_owner": bot.owner,
            "additional_owners": bot.extra_owners,
            "webAuth": "None",
            "webURL": "None",
            "webhook": "None",
            "token": secrets.token_urlsafe()
        })
    await app.mongo.bots.update_one({"botID": bot.bot_id}, {"$set": {"type": "approved"}})

async def deny(app, bot):
    ...
