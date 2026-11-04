import aiohttp
import random
from random import randint


async def get_cat_gif(ctx,GIPHY_API_KEY):
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


async def get_general_gif(ctx, suche, GIPHY_API_KEY):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.giphy.com/v1/gifs/search",
            params={
                "api_key": GIPHY_API_KEY,
                "q": suche,
                "limit": 20,
                "rating": "pg-13",
            },
        ) as resp:
            if resp.status != 200:
                await ctx.send("Die GIF-Suche hat gerade ein Problem.")
                return
            data = await resp.json()

    ergebnisse = data.get("data", [])
    if not ergebnisse:
        await ctx.send(f"Kein GIF zu „{suche}“ gefunden.")
        return

    await ctx.send(random.choice(ergebnisse)["url"])