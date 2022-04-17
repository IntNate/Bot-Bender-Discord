from tickets import Tickets
import discord
from discord.ext import commands
import asyncio
import time
import random
import glob
import requests
from bs4 import BeautifulSoup
import json


with open('token.json', 'r+') as file:
    token = json.load(file)



intents = discord.Intents.default()
intents.members = True


normal = Tickets("normal", 30, 100)
plus = Tickets("plus", 15, 450)
premium =Tickets("premium", 5, 1000)

# token = "OTU5OTkxODQ5NjAxMzUxNzIy.Ykj8FA.hbbfmgEgS37KyNSpZtqBxtY2wQs"
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


@bot.command(aliases=['bible','genèse'])
async def genese(ctx):
    url = 'https://www.bibleenligne.com/bible/gn.html'
    r = requests.get(url)


    soup = BeautifulSoup(r.text,  features="lxml")
    verset = soup.find_all(class_='verset')

    verset_number = random.randint(0, 1532)
    await ctx.reply(verset[verset_number].text)

@bot.command()
async def nate(ctx):
    nate = ['Nate est un génie.',
            'Nate est un grand écrivain.',
            'Nate aime uniquement les femmes.',
            'Nate a des cheveux soyeux.',
            'Nate est fort sympathique.',
            'Nate est un grand orateur.',
            'Nate a de jolis yeux.',
            'Nate est modeste.',
            'Nate est altruiste.',
            'Nate est adorable.',
            'Nate est dynamique.',
            'Nate est élégant.',
            'Nate est romantique.',
            'Nate est diplomate.',
            'Nate est mignon.']
    await ctx.reply(random.choice(nate))


async def check_nfsw(ctx):
    if ctx.channel.is_nsfw() == True:
        return True
    else:
        return False
    
    
    

@bot.command(aliases=['nudes'])
async def nude(ctx):
    if await check_nfsw(ctx) == False:
        nude.error()
        
    url = 'https://www.balancetanude.fr/category/photos-snaps-18/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text,  features="lxml")
    max_page = soup.find_all(class_='page-numbers')
    max_page = max_page[7].text[4:8]

    random_page = random.randint(1, int(max_page))
    url2 = f'https://www.balancetanude.fr/category/photos-snaps-18/page/{random_page}/'
    r2 = requests.get(url2)

    got = False
    while got == False:
        
        random_image = random.randint(1,29)
        soup3 = BeautifulSoup(r2.text,  features="lxml")
        nude_name = soup3.find_all(class_='entry-title')
        try :
            nude_name = nude_name[random_image].find('a')
            nude_name = nude_name.text
            got = True
        except(IndexError):
            pass

    #lien
    soup4 = BeautifulSoup(r2.text,  features="lxml")
    nude_link = soup4.find_all(class_='entry-title',)
    nude_link = nude_link[random_image].find('a')['href']
    #get nudes
    str(nude_link)
    url3 = nude_link

    #image
    url3 = nude_link
    r3 = requests.get(url3)
    soup5 = BeautifulSoup(r3.text, features="lxml")
    nude_image = soup5.find_all('img')
    nude_image = nude_image[1]['src']
    
    logo = 'https://www.balancetanude.fr/wp-content/uploads/2020/11/logo.webp'
    
    embed = discord.Embed(
    
        title = f'{nude_name}',
        description = f'[Lien]({nude_link})',
        colour = discord.Colour.red()
    )
    embed.set_image(url=nude_image)
    embed.set_thumbnail(url=logo)
    embed.set_author(name=f'',icon_url=logo)
    
    await ctx.reply(embed=embed)
    
    
@nude.error
async def on_command_error(ctx, error):
    await ctx.reply('Vous devez être dans un salon NFSW pour utiliser cette commande !')


bot.run(token['token'])