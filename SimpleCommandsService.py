from random import randint

async def getMM(ctx):
    
    randomNumber = randint(1,100)
    
    if(1 <= randomNumber <= 25):
        await ctx.send("Ja!")
    elif(26 <= randomNumber <= 50):
        await ctx.send("Nein!")
    elif(51 <= randomNumber <= 75):
        await ctx.send("Vielleicht")
    else:
        await ctx.send("Frag mich nochmal in einer Stunde")