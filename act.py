# List specific code for IBL
#
# Replace this with code for your specific list

# Routes should be self-explanatory
import motor.motor_asyncio
import os
import secrets
import re
import datetime
import discord
import utils
import asyncio

modlogs = 911907978926493716

async def prepare(app):
    """This sets up the mongodb database. It is a TODO"""
    # TODO: ask toxic if this is correct?
    app.mongo = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGO_URL"))[os.environ.get("MONGO_DBNAME")]

async def claim(app, bot, _secrets):
    _bot = await app.mongo.bots.find_one({"botID": bot.bot_id})
    if not _bot:
        # We do not want to send any thing or do anything in claim/unclaim/deny if bot does not already exist
        return
    
    if _bot.get("type") != "pending" or not _bot.get("type"):
        print("Ignoring")
        return

    # Hopefully
    await app.mongo.bots.update_one({"botID": bot.bot_id}, {"$set": {"claimed": True, "claimedBy": bot.reviewer}})
    
    # TODO: ask toxic to make a proper claim embed

async def unclaim(app, bot, _secrets):
    _bot = await app.mongo.bots.find_one({"botID": bot.bot_id})
    if not _bot:
        # We do not want to send any thing or do anything in claim/unclaim/deny if bot does not already exist
        return

    if bot["type"] != "pending":
        print("Ignoring")
        return
    
    await app.mongo.bots.update_one({"botID": bot.bot_id}, {"$set": {"claimed": False, "claimedBy": ""}})

async def approve(app, bot, _secrets):
    _bot = await app.mongo.bots.find_one({"botID": bot.bot_id})
    if not _bot:
        if not _bot.cross_add:
            print("Not cross addable")
            return
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
            "short": bot.description,
            "long": bot.long_description,
            "tags": ", ".join(bot.tags),
            "invite": bot.invite or f"https://discord.com/oauth2/authorize?client_id={bot.bot_id}&permissions=0&scope=bot%20applications.commands",
            "main_owner": bot.owner,
            "additional_owners": bot.extra_owners,
            "webAuth": "None",
            "webURL": "None",
            "webhook": "None",
            "token": secrets.token_urlsafe(),
            "type": "pending"
        })

        _bot = {"type": "pending"}

    if _bot.get("type") != "pending" or not _bot.get("type"):
        print("Ignoring")
        return

    await app.mongo.bots.update_one({"botID": bot.bot_id}, {"$set": {"type": "approved"}})

    embed = discord.Embed(title="**__Bot Approved:__**", color=discord.Color.from_rgb(19, 76, 173))
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/815094858439065640/972734471369527356/FD34E31D-BFBC-4B96-AEDB-0ECB16F49314.png")
    embed.add_field(name="Bot:", value=f"<@{bot.bot_id}>", inline=True)
    embed.add_field(name="Owner:", value=f"<@{bot.owner}>", inline=True)
    embed.add_field(name="Moderator:", value=f"<@{bot.reviewer}>", inline=True)
    embed.add_field(name="Feedback:", value=f"{bot.reason}", inline=True)
    embed.set_footer(text="© Copyright 2021 - 2022 - Metro Reviewers")
    embed.timestamp = datetime.datetime.now()

    asyncio.create_task(utils.msg_sender(_secrets["token"], modlogs, embed))

async def deny(app, bot, _secrets):
    _bot = await app.mongo.bots.find_one({"botID": bot.bot_id})
    if not _bot:
        # We do not want to send any thing or do anything in claim/unclaim/deny if bot does not already exist
        return

    if _bot.get("type") != "pending" or not _bot.get("type"):
        print("Ignoring")
        return

    await app.mongo.bots.update_one({"botID": bot.bot_id}, {"$set": {"type": "denied"}})

    embed = discord.Embed(title="**__Bot Denied :(:__**", color=discord.Color.from_rgb(19, 76, 173))
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/815094858439065640/972734471369527356/FD34E31D-BFBC-4B96-AEDB-0ECB16F49314.png")
    embed.add_field(name="Bot:", value=f"<@{bot.bot_id}>", inline=True)
    embed.add_field(name="Owner:", value=f"<@{bot.owner}>", inline=True)
    embed.add_field(name="Moderator:", value=f"<@{bot.reviewer}>", inline=True)
    embed.add_field(name="Reason:", value=f"{bot.reason}", inline=True)
    embed.set_footer(text="© Copyright 2021 - 2022 - Metro Reviewers")
    embed.timestamp = datetime.datetime.now()

    asyncio.create_task(utils.msg_sender(_secrets["token"], modlogs, embed))
