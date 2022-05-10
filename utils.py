import aiohttp

async def msg_sender(token, channel, embed):
    async with aiohttp.ClientSession() as sess:
        async with sess.post(
            f"https://discord.com/api/v10/channels/{channel}/messages",
            json={
                "embeds": [embed.to_dict()]
            },
            headers={
                "Authorization": f"Bot {token}",
                "User-Agent": "Catnip/0.1"
            }
        ) as resp:
            print(resp.status)
            json = await resp.json()
            print(json)
