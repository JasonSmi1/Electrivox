from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import events

load_dotenv()

TOKEN = os.getenv('TOKEN')
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user.name}')

async def on_message(bot, message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Process commands
    await bot.process_commands(message)

# Define the role names and emoji reactions
roles = {
    'Role 1': '🛡️',
    'Role 2': '⚔️',
    'Role 3': '🌳'
}

# Function to check and assign roles based on reactions
@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 1114635657009168545: # Copy a message ID in Discord and paste here
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = None

        for role_name, emoji in roles.items():
            if str(payload.emoji) == emoji:
                role = discord.utils.get(guild.roles, name=role_name)
                break

        if role is not None:
            await member.add_roles(role)

# Function to check and remove roles when reactions are removed
@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == 1114635657009168545: # Copy a Discord message ID and paste here
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = None

        for role_name, emoji in roles.items():
            if str(payload.emoji) == emoji:
                role = discord.utils.get(guild.roles, name=role_name)
                break

        if role is not None:
            await member.remove_roles(role)

# Command to post the event and add role reactions
@bot.command()
async def post_event(ctx):
    event_message = await ctx.send("Event details here")

    for emoji in roles.values():
        await event_message.add_reaction(emoji)

# Run the bot
bot.run(TOKEN)
