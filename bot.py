from tickets import Tickets
import discord
from discord.ext import commands
import asyncio
import time
import random
import glob
import requests

intents = discord.Intents.default()
intents.members = True


normal = Tickets("normal", 30, 100)
plus = Tickets("plus", 15, 450)
premium =Tickets("premium", 5, 1000)

token = "OTU5OTkxODQ5NjAxMzUxNzIy.Ykj8FA.hbbfmgEgS37KyNSpZtqBxtY2wQs"
bot = commands.Bot(command_prefix="?", intents=intents)


data = {

    "id"    :   "dette",
    299956001573044224 : 0,
    }


pute_list = []


async def check_id(ctx, id):
    
    if id not in data:
        print(data)
        data[id] = 0


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Préfix : ?"))


@bot.command()
async def test(ctx, what):
    await ctx.send(f"test {what}")


@bot.command()
async def buy(ctx, ticket):
    
    list_tickets= ["normal","plus", "premium"]
    reward = 10000
    author = ctx.message.author.mention
    id = ctx.message.author.id
    
    await check_id(ctx, id)
    if ticket not in list_tickets:
        await buy.error()
    
    elif ticket == "normal":
        result = normal.play()
        data[id] += normal.price
    
    elif ticket == "plus":
        result = plus.play()
        data[id] += plus.price
    
    elif ticket == "premium":
        result = premium.play()
        data[id] += premium.price
    
    
    message = await ctx.send(f"{author} a lancé la machine...")
    
    
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
            await ctx.send(f"{author} tu as gagné {reward} G ! 🤩")
            data[id] -= reward
            
            
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
        await ctx.send(f"{author} tu as perdu... :pensive:")
    

@buy.error
async def on_command_error(ctx, error):
    await ctx.send("""```Erreur de syntaxe\n
syntaxe :!buy   <ticket>\n   
                normal\n
                plus\n
                premium```""")

@bot.command(aliases=["debt"])
async def dette(ctx, member: discord.Member=""):
    
    if member == "":
        member = ctx.message.author
        await check_id(ctx, ctx.message.author.id)
        member_wallet = data[ctx.message.author.id]
        if member_wallet > 0:
            await ctx.send(f"Votre dette s'élève à {member_wallet} G 🪙")
        elif member_wallet == 0:
            await ctx.send(f"Vous n'avez aucune dette ! 🪙")
        elif member_wallet < 0:
            await ctx.send(f"Le serveur vous doit {'{:}'.format(abs(member_wallet))} G 🪙")

    else:
        await check_id(ctx, member.id)
        member_wallet = data[member.id]
        
        
        if member_wallet > 0:
            await ctx.send(f"la dette de {member.mention} est de {member_wallet} G 🪙")
        elif member_wallet == 0:
            await ctx.send(f"La dette de {member.mention} s'élève à {member_wallet} G 🪙")
        elif member_wallet < 0:
            await ctx.send(f"Le serveur doit à {member.mention} {'{:}'.format(abs(member_wallet))} G 🪙")
    

@bot.command(aliases=["probas"])
async def proba(ctx, *, what):
    await ctx.reply(f"les probabilités sont de {random.randint(0,100)}%")


@bot.command()
async def pute(ctx, member:discord.Member):
    
    if str(member) not in pute_list:
        await ctx.reply(f"{member.mention} a été ajouté à la liste des putes du serveur avec succès ✅")
        pute_list.append(str(member))
    
    else:
        await ctx.reply(f"{member.mention} est déjà dans la liste des putes du serveur")
    

@bot.command(aliases=["putelist","puteliste","listepute","putelistes"])
async def listputes(ctx):
    
    x = "\n".join(pute_list)
    await ctx.reply(f"liste des putes : \n{x}")
    

@bot.command(aliases=["pay"])
async def refund(ctx, member:discord.Member, amount):
    await check_id(ctx, ctx.message.author.id)
    
    if amount == "all":
        if data[member.id] < 0:
            await ctx.reply("L'utilisateur est déjà en positif !")
        elif data[member.id] > 0:
            data[member.id] = 0
            await ctx.reply(f"La dette de {member} a été remise à 0 🪙")
        
    else:
        try:
            int(amount)

        except(ValueError):
            await ctx.reply("Montant non reconnu. Réessayez")
        
        else:
            data[member.id] = data[member.id] - int(amount)
            await ctx.reply(f"La dette de {member} a été réduite de {amount} G 🪙")
           
@bot.command(aliases=["sex","seggs"])
async def sexe(ctx, member:discord.Member=""):
    list_members = ctx.message.guild.members
    random_members = (list_members[random.randint(0, (len(list_members) - 1))])
    if member == "":
        member = ctx.message.author
    
    await ctx.send(f"{member.mention} doit faire le sexe avec {random_members.mention} 😳🔞")
    
 
@bot.command()
async def mp(ctx, member:discord.Member, *, msg):
    await ctx.message.delete()
    user = bot.get_user(member.id) or await bot.fetch_user(member.id)
    sender = bot.get_user(ctx.message.author.id) or await bot.fetch_user(ctx.message.author.id)
    try:
        await user.send(f"Tu as reçu un message anonyme ! 💌\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n{msg}")
        await sender.send("le message a bien été envoyé ! 💌")
    except:
        await sender.send("l'utilisateur n'a pas pu recevoir ton message 😟")
    
    
@bot.command(aliases=["meow","chat"])
async def miaou(ctx):    

    file_path_type = ["./chatent/*.png", "./chatent/*.jpg","./chatent/*.jpeg"]
    images = glob.glob(random.choice(file_path_type))
    random_image = random.choice(images)

    await ctx.reply("meow :cat:", file=discord.File(random_image))


@bot.command(aliases=["who"])
async def qui(ctx, *,sentence):
    list_members = ctx.message.guild.members
    random_members = (list_members[random.randint(0, (len(list_members) - 1))])
    await ctx.reply(f'celui qui {sentence} est {random_members.mention}')
    

@bot.command()
async def question(ctx):    
    x = random.randint(0,1)
    oui_list = ["oui", "très clairement", "absolument", "c'est sûr","tout à fait", "certainement"]
    non_list = ["non", "absolument pas", "pas du tout", "c'est impossible", "aucunement", "nope"]
    if x == 0:
        await ctx.reply(random.choice(non_list))
    else:
        await ctx.reply(random.choice(oui_list))
    

@bot.command(aliases=['r'])
async def risibank(ctx):
    check = False
    while check == False:
        
        risibank_logo = 'https://risibank.fr/logo.png'
        url = 'https://risibank.fr/api/v1/medias/random?only_one=true'
        r = requests.get(url).json()
        rjson = r[0]
        image = rjson['source_url']
        author_id = rjson['user_id']
        
        url2 = f'https://risibank.fr/api/v1/users/{author_id}/collections'
        r2 = requests.get(url2).json()
        r2json = r2[0]
        author_name = r2json['user']['username_custom']
        
        image_id = rjson['id']
        image_tag = rjson['slug']
        
        if rjson['source_exists'] == True and rjson['is_deleted'] == False:
            check = True
        
    embed = discord.Embed(
    
        title = f'Auteur : {author_name}',
        description = f'[Lien RisiBank](https://risibank.fr/media/{image_id}-{image_tag})',
        colour = discord.Colour.blue()
    )
    embed.set_image(url=image)
    embed.set_thumbnail(url=risibank_logo)
    embed.set_author(name='Image aléatoire venant de RisiBank :',icon_url='')
    
    await ctx.reply(embed=embed)


bot.run(token)