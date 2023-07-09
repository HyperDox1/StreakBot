import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
client.remove_command("help")
TOKEN = os.getenv("DISCORD_TOKEN")
bot_status = cycle(['Continue your streak!'])

@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))

@client.event
async def on_ready():
    await client.tree.sync()
    print(f'Success! {client.user} is now connected!')
    change_status.start()

@client.listen()
async def on_message(message):
    if message.author.bot is False and "happy sabbath" in message.content.lower():
        await message.reply("Happy Sabbath!")

@client.tree.command(name="hello", description="Gives a nice greeting") #forward slash / command
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("What's up!")

#load cogs into the bot
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with client:
        await load()
        await client.start(TOKEN)

asyncio.run(main())
