import asyncio
import discord
from src.response import ResponseGenerator
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import time

intents = discord.Intents(messages=True, guilds=True, typing = False, presences = False, members=False)
config_general=json.loads(open("config-bot.json","r").read())
client = discord.AutoShardedClient(intents=intents, chunk_guilds_at_startup=False,command_prefix=str(config_general["prefix"]))


model=ResponseGenerator("https://woz-model.herokuapp.com/v1/models/jade:predict","https://discord.com/api/webhooks/806950915449683970/-8IG5UkdBGf7jgfQ36XlfRSIUjt2V-rt-RNn9NdC3zDgfvjzMS2SEMj-XlozsXH9Ovju")

@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+str(client.user.id)+') | Connected to '+str(len(client.guilds))+' servers')
    print('--------')
    print("Discord.py verison: " + discord.__version__)
    print('--------')
    print(str(len(client.shards))+" shard(s)")
    
@client.event
async def on_message(message):
    loop = asyncio.get_event_loop()
    
    if message.author.bot == False and message.guild != None:
        try:
            bot.process_commands(message)
        except:
            message.content.lower().startswith(config_general["prefix"]):
            msg=message.content
            tomodel_message=msg.replace(config_general["prefix"],"")
            async with message.channel.typing():
                    out = await loop.run_in_executor(ThreadPoolExecutor(), model.response, message.author, tomodel_message, True)
                await message.reply(out.replace("@everyone","").replace("@here", ""))
                                   
                                    
@bot.command(aliases=['-r'])
async def _res(ctx):
    model.reset(message.author.id)
    await message.reply("Successfully reset your history with Jade")
                                    
@bot.command(aliases=['-h'])
async def _hist(ctx):
    ogs=model.register(message.author.id, time.time())
    await message.reply("History:\n> "+"\n> ".join(logs["history"])+f"\nLast seen: {datetime.fromtimestamp(logs['timestamp'])}")




client.run(config_general["token"])
