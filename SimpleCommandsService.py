import random
from random import randint


async def get_MM(ctx):
    
    random_number = randint(1,100)
    
    if(1 <= random_number <= 25):
        await ctx.send("Ja!")
    elif(26 <= random_number <= 50):
        await ctx.send("Nein!")
    elif(51 <= random_number <= 75):
        await ctx.send("Vielleicht")
    else:
        await ctx.send("Frag mich nochmal in einer Stunde")

async def get_sleep_message(ctx):

    emote_array = ["<:sleepfox:1388235331278737408>"
                   ,"<:cuddlefox:1388235306385539074>"
                   ,"<:FoxMuedlich:1459242100683046933>"
                   ,"<:FoxBaeriiii:1459241885033037879>"]

    await ctx.send("Gute Nacht. " + random.choice(emote_array))