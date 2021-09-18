import discord
from discord.ext import commands
from config import settings
import music

client = commands.Bot(command_prefix=settings['prefix'], intents=discord.Intents.all())

cogs = [music]

for i in range(len(cogs)):
    cogs[i].setup(client=client)

client.run(settings['token'])
