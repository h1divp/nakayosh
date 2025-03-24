import discord
import asyncio
from discord.ext import commands #, app_commands
import logging
import os
from dotenv import dotenv_values

config = dotenv_values(".env")
GUILDS = config['GUILDS'].split(",")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
description = "In the コーナー"

bot = commands.Bot(command_prefix=config['PREFIX'], description=description, intents=intents)
logger = logging.FileHandler(filename=config['LOG_FILENAME'], encoding='utf-8', mode='w')

@bot.event
async def on_ready():
    game = discord.Game("shiritori")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print(f'Logged on as {bot.user}.')

async def load_extensions(bot):
  for filename in os.listdir("./src/cogs/"):
      if filename.endswith(".py"):
          print(f"loaded cog {filename[:-3]}")
          await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_extensions(bot)
        await bot.start(config['TOKEN'])

# print(os.getcwd())
asyncio.run(main())
