import os
import aiohttp
import discord
import random
from random import randint
from discord.ext import tasks, commands


DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])
TWITCH_CLIENT_ID = os.environ["TWITCH_CLIENT_ID"]
TWITCH_CLIENT_SECRET = os.environ["TWITCH_CLIENT_SECRET"]
STREAMER = os.environ["STREAMER"].lower()
GIPHY_API_KEY = os.environ["GIPHY_API_KEY"]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="?", intents=intents)

twitch_token = None
was_live = False


async def get_twitch_token(session):
    """Holt einen App Access Token (Client-Credentials-Flow)."""
    async with session.post(
        "https://id.twitch.tv/oauth2/token",
        params={
            "client_id": TWITCH_CLIENT_ID,
            "client_secret": TWITCH_CLIENT_SECRET,
            "grant_type": "client_credentials",
        },
    ) as resp:
        data = await resp.json()
        return data["access_token"]


async def fetch_stream(session):
    """Gibt die Stream-Daten zurück oder None, wenn offline."""
    global twitch_token
    if twitch_token is None:
        twitch_token = await get_twitch_token(session)

    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {twitch_token}",
    }
    async with session.get(
        "https://api.twitch.tv/helix/streams",
        params={"user_login": STREAMER},
        headers=headers,
    ) as resp:
        if resp.status == 401:  # Token abgelaufen -> beim nächsten Durchlauf neu holen
            twitch_token = None
            return None
        data = await resp.json()
        return data["data"][0] if data.get("data") else None


@tasks.loop(seconds=60)
async def check_stream():
    global was_live
    async with aiohttp.ClientSession() as session:
        stream = await fetch_stream(session)

    is_live = stream is not None
    if is_live and not was_live:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(
                f"🔴 **{stream['user_name']}** ist jetzt live!\n"
                f"**{stream['title']}** – Spiel: {stream['game_name']}\n"
                f"https://twitch.tv/{STREAMER}\n"
                f"@everyone"
            )
    was_live = is_live


@bot.event
async def on_ready():
    print(f"Eingeloggt als {bot.user}")
    if not check_stream.is_running():
        check_stream.start()


@bot.command()
async def ping(ctx):
    """pong"""
    await ctx.send("pong")
    
    
@bot.command()
async def mm(ctx):
    """Die magische Miesmuschel"""
    randomNumber = randint(1,100)
    
    if(1 <= randomNumber <= 25):
        await ctx.send("Ja!")
    elif(26 <= randomNumber <= 50):
        await ctx.send("Nein!")
    elif(51 <= randomNumber <= 75):
        await ctx.send("Vielleicht")
    else:
        await ctx.send("Frag mich nochmal in einer Stunde")

@bot.command()
async def cat(ctx):
    """Gibt ein Katzen Gif aus"""
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.giphy.com/v1/gifs/search",
            params={
            "api_key": GIPHY_API_KEY,
            "q": "cat",
            "limit": 50,
            "rating": "pg-13",
            },
        ) as resp:
            if resp.status != 200:
                await ctx.send("GIF konnt nicht geladen werden :(")
                return
            data = await resp.json()
    ergebnisse = data.get("data",[])
    
    if not ergebnisse:
        await ctx.send("Keine Katzen gefunden")
        return
    
    await ctx.send(random.choice(ergebnisse)["url"])

@bot.command()
async def night(ctx):
    """Gint ein gute Nacht Gif aus"""
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.giphy.com/v1/gifs/search",
            params={
            "api_key": GIPHY_API_KEY,
            "q": "good night",
            "limit": 20,
            "rating": "pg-13",
            },
        ) as resp:
            if resp.status != 200:
                await ctx.send("GIF konnt nicht geladen werden :(")
                return
            data = await resp.json()
    ergebnisse = data.get("data",[])
    
    if not ergebnisse:
        await ctx.send("Keine Gute Nacht gefunden")
        return
    
    await ctx.send(random.choice(ergebnisse)["url"])

bot.run(DISCORD_TOKEN)


















