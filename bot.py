import os
import discord
import GifService
import SimpleCommandsService as SCS
from TwitchService import TwitchService
from discord.ext import tasks, commands


DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])
TWITCH_CLIENT_ID = os.environ["TWITCH_CLIENT_ID"]
TWITCH_CLIENT_SECRET = os.environ["TWITCH_CLIENT_SECRET"]
STREAMER = os.environ["STREAMER"].lower()
GIPHY_API_KEY = os.environ["GIPHY_API_KEY"]

intents = discord.Intents.default()
intents.message_content = True
BOT = commands.Bot(command_prefix="?", intents=intents)

twitch_service = TwitchService(TWITCH_CLIENT_ID,TWITCH_CLIENT_SECRET,STREAMER,CHANNEL_ID,BOT)

@tasks.loop(seconds=60)
async def check_stream():
    await twitch_service.check_stream()

@BOT.event
async def on_ready():
    print(f"Eingeloggt als {BOT.user}")
    if not check_stream.is_running():
        check_stream.start()

@BOT.command()
async def ping(ctx):
    """pong"""
    await ctx.send("pong")    
    
@BOT.command()
async def mm(ctx):
    """Die magische Miesmuschel"""
    await SCS.get_MM(ctx)

@BOT.command()
async def cat(ctx):
    """Gibt ein Katzen Gif aus"""
    await GifService.get_cat_gif(ctx,GIPHY_API_KEY)

@BOT.command()
async def gif(ctx,*,search):
    """Gibt ein passendes Gif aus: ?gif [Text]"""
    await GifService.get_general_gif(ctx,search,GIPHY_API_KEY)

@BOT.command()
async def sleep(ctx):
    """Sendet eine gute Nacht Nachricht"""
    await SCS.get_sleep_message(ctx)

@BOT.command()
async def fact(ctx):
    """Gibt einen Zufallsfakt aus"""
    await SCS.get_random_facts(ctx)

BOT.run(DISCORD_TOKEN)