# List specific code for IBL
#
# Replace this with code for your specific list

# Routes should be self-explanatory

async def claim(app, bot):
    bot = await app.mongo.bots.find_one({"botID": bot.bot_id})
    if not bot:
        # We do not want to send any thing or do anything in claim/unclaim/deny. Maybe approve but thats for toxic to decide
        # TODO: Ask toxic
        return
    
    # Hopefully
    await app.mongo.bots.update_one({"botID": bot.bot_id}, {"$set": {"claimed": True, "claimedBy": bot.reviewer}})
    
    # TODO: ask toxic to make a proper claim embed

async def unclaim(app, bot):
    ...

async def approve(app, bot):
    ...

async def deny(app, bot):
    ...
