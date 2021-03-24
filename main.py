import discord
import os
import requests as req
from dotenv import load_dotenv  
from pokemontcgsdk import Type, Rarity, Subtype

def get_query(message):
   query="?q=supertype:pokemon"
   for i in message:
       query=query+" "+i
   return query

def get_data(query):
    json = get_json(query)
    data=list(json.values())[0]
    if len(data) >= 10:
        return 0
    if not data:
        return None
    else:
        return data

def get_json(query):
    response = req.get("https://api.pokemontcg.io/v2/cards" + query)
    if response.status_code != 200:
        return None
    else: 
        return response.json()

def get_image(data):
    images=[]
    for i in data:
        for a,b in i.items():
            if a=='images':
                for cock,balls in b.items():
                    if cock=='small':
                        images.append(balls)
    return images

def get_price(data):
    prices=[]
    for i in data:
        for a,b in i.items():
            if a=='tcgplayer':
                for cock,balls in b.items():
                    if (cock=='prices'):
                        prices.append(list(balls.items())[0])       
    return prices
    
def prettify(prices):
    pretty=""
    for b in prices:
        title=""
        cardprices=""
        if type(b) != dict:
            title+=("     -- %s -- \n" % b.upper())
            card=title
        else:
            for k,v in b.items():
                if k.lower() != 'directlow':
                    cardprices+=("%s : $%s  |   " % (k.upper(), v))
        card+=cardprices
    return card
'''
message="-cardprice types:water"
message=message.split(" ")
message.pop(0)
query= get_query(message)
data= get_data(query)
print(data)

'''

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
            await message.channel.send("You fucked something up in your command.. check pinned messages for correct format")
        else:
            image = get_image(data)
            prices= get_price(data)
            for i in range(len(prices)):
                card=prettify(prices[i])
                await message.channel.send(image[i])
                await message.channel.send(card)
        

client.run(TOKEN)
