from ctypes import resize
import tickets
import discord
from discord.ext import commands
import asyncio
import time
import random

normal = tickets.Tickets("normal", 30)
plus = tickets.Tickets("plus", 15)
premium = tickets.Tickets("premium", 5)



token = "OTU5OTkxODQ5NjAxMzUxNzIy.Ykj8FA.-YesWwQNdltUozW8GhpSRBd3xDk"
bot = commands.Bot(command_prefix="?")


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Préfix : ?"))



@bot.command()
async def test(ctx, what):
    await ctx.send(f"test {what}")



@bot.command()
async def buy(ctx, ticket):
    
    list_tickets= ["normal","plus", "premium"]
    
    author = ctx.message.author.mention
    message = await ctx.send(f"{author} a lancé la machine...")
    
    if ticket not in list_tickets:
        await buy.error()
    elif ticket == "normal":
        result = normal.play()
    elif ticket == "plus":
        result = plus.play()
    elif ticket == "premium":
        result = premium.play()
        
    
        
        
       
        
        
        
    
    
    
    if result == True:
            await asyncio.sleep(1)
            await message.edit(content=":white_large_square::white_large_square::white_large_square:")
            await asyncio.sleep(0.5)
            await message.edit(content="⭐:white_large_square::white_large_square:")
            await asyncio.sleep(0.5)
            await message.edit(content="⭐⭐:white_large_square:")
            await asyncio.sleep(0.5)
            await message.edit(content="⭐⭐⭐")
            await asyncio.sleep(0.5)
            await ctx.send("Vous avez gagné ! 🤩")
    
    
    
    
    else:
        
        
        await asyncio.sleep(1)
                
                
        list_emoji = ["❌", "❌", "❌","⭐","⭐"]  
        random.shuffle(list_emoji)
        await message.edit(content=":white_large_square::white_large_square::white_large_square:")        
        await asyncio.sleep(0.5)
        await message.edit(content=f"{list_emoji[0]}:white_large_square::white_large_square:")
        await asyncio.sleep(0.5)
        await message.edit(content=f"{list_emoji[0]}{list_emoji[1]}:white_large_square:")
        await asyncio.sleep(0.5)
        await message.edit(content=f"{list_emoji[0]}{list_emoji[1]}{list_emoji[2]}")
        await asyncio.sleep(0.5)
                
                
                
        await ctx.send("Vous avez perdu ! :pensive:")
    
    
    
    # await ctx.send(author)
    
    
    
    
# @buy.error
# async def on_command_error(ctx, error):
#     await ctx.send("ERROR")






bot.run(token)