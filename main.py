import discord
from discord.ext import commands
import os
import requests as req
from dotenv import load_dotenv  
from pokemontcgsdk import Type, Rarity, Subtype


def get_data(arg):
    json = get_json(arg)
    if not json:
        return None
    else:
        data=list(json.values())[0]
        return 0 if len(data) >= 20 else data

def get_json(arg):
    response = req.get("https://api.pokemontcg.io/v2/cards?q=" + arg)
    return None if response.status_code != 200 else response.json()

def get_image(data):
    images=[]
    [[images.append(p) for c,p in b.items() if c=='small']for i in data for a,b in i.items() if a=='images']
    return images

def get_price(data):
    tcgplayer=[]
    prices=[]
    tcgplayer = [tcgplayer+list(b.items()) for i in data for a,b in i.items() if a=='tcgplayer']
    prices = [list(p.items()) for g in tcgplayer for c,p in g if c=='prices']
    return prices
    
def prettify(price):
    card=""
    title=""
    cardprices=""
    title = [title+("\n -- %s -- \n" % x.upper())for i in range(len(price)) for x in price[i] if type(x) != dict]
    cardprices= [[cardprices+("|   %s : $%s  |   " % (k.upper(), v)) for k,v in x.items() if k.lower() != 'directlow']for i in range(len(price)) for x in price[i] if type(x) == dict]
    for i in range(len(title)):
        card+=title[i]    
        for q in range(len(cardprices[i])):
            card += str(cardprices[i][q])
    return card

load_dotenv()
TOKEN = os.getenv('TOKEN')
intents = discord.Intents.all()
client= commands.Bot(command_prefix='-', intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command()
async def types(ctx):
    types = Type.all()
    await ctx.send(types)

@client.command()
async def subtypes(ctx):
    subtypes = Subtype.all()
    await ctx.send(subtypes)

@client.command()
async def attributes(ctx):
    attributes="set.name:<set name>, name:<pokemon name>, rarity:<rarity>, subtypes:<subtypes> , types:<pokemon type>"
    await ctx.send(attributes)

@client.command()
async def rarity(ctx):
    rarities = Rarity.all()
    await ctx.send(rarities)

@client.command()
async def cardprice(ctx, *, arg):
    data= get_data(arg)
    if data == 0:
        await ctx.send("Result waay too big, narrow down the search")
    elif not data:
        await ctx.send("Error in your command.. check pinned messages for correct format")
    else:
        image = get_image(data)
        prices= get_price(data)
        for i in range(len(image)):
            card=prettify(prices[i])
            await ctx.send(image[i])
            await ctx.send(card)

client.run(TOKEN)
