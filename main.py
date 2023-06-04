# Meant for WoW Wrath of the Lich King,
# But really it will evolve into any event creator and inviter

from dotenv import load_dotenv
import os
import discord
import commands

load_dotenv()  # Load environment variables from .env file

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(TOKEN)
