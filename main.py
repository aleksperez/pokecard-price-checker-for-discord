import discord
import os
import requests as req
from dotenv import load_dotenv  
from pokemontcgsdk import Type, Rarity, Subtype

def get_query(message):
   query="?q="
   for i in message:
       query=query+" "+i
   return query

def get_data(query):
    json = get_json(query)
    if not json:
        return None
    else:
        data=list(json.values())[0]
        return 0 if len(data) >= 20 else data

def get_json(query):
    response = req.get("https://api.pokemontcg.io/v2/cards" + query)
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
client=discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("-types"):
        types = Type.all()
        await message.channel.send(types)

    if message.content.startswith("-subtypes"):
        subtypes = Subtype.all()
        await message.channel.send(subtypes)

    if message.content.startswith("-attributes"):
        attributes=["set.name:<set name>","name:<pokemon name", "rarity:<rarity>", "subtypes:<subtypes>" , "types:<pokemon type>"]
        await message.channel.send(attributes)

    if message.content.startswith("-rarity"):
        rarities = Rarity.all()
        await message.channel.send(rarities)

    if message.content.startswith('-cardprice'):
        mes = message.content.split(" ")
        mes.pop(0)
        query= get_query(mes)
        data= get_data(query)
        if data == 0:
            await message.channel.send("Result waay too big, narrow down the search")
        elif not data:
            await message.channel.send("Error in your command.. check pinned messages for correct format")
        else:
            image = get_image(data)
            prices= get_price(data)
            for i in range(len(image)):
                card=prettify(prices[i])
                await message.channel.send(image[i])
                await message.channel.send(card)
client.run(TOKEN)
