import json 
from discord.ext import commands
import os
import discord
with open('config/values.json', 'r') as f:
    data = json.load(f)
    client = commands.Bot(command_prefix=commands.when_mentioned_or(f"{data['prefix']}"), case_insensitive=True, intents=discord.Intents.default())
    client.remove_command('help')

@client.event 
async def on_ready():
    print('Ya estoy en linea')

for filename in os.listdir('./files'):
  if filename.endswith('.py'):
      client.load_extension(name=f'files.{filename[:-3]}')

client.run(data['token'])