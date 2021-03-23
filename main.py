import discord
import os
import requests as req
from dotenv import load_dotenv  

def get_response(detail,query=None):
    if query!=None:
        response = req.get("https://api.pokemontcg.io/v2/"+ detail +query)
    else:
        response = req.get("https://api.pokemontcg.io/v2/"+ detail)
        if response.status_code != 200:
            raise ApiError('GET /tasks/ {}'.format(response.status_code))
        else: 
            return response.json()
        
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

    if message.content.startswith('-card'):
       
        await message.channel.send()

client.run(TOKEN)
'''
attributes=["name","type", "subtype", "rarity"]

def get_query(message):
    if any(word in message for word in attributes):
        query=
    query = message.split("name",1)[1]
    return query

message="-card name:Aerodactyl type:Rare"
message=message.split(" ")
print(get_name(message))

def get_sets():
    setnames=[]
    fullJson= get_response("sets")
    for k,v in fullJson.items():
        if type(v) == int:
            break
        else: 
            for pokeset in v:
                for a,b in pokeset.items():
                    if a =='name':
                        setnames.append(b)
    return setnames



def get_subtypes():
    pass

def get_supertypes():
    pass

def get_rarities():
    pass


