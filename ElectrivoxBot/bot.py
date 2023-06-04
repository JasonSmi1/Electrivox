from tabnanny import check
import asyncio
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from events import Event


class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create_event(self, ctx):
        try:
            # Wait for the event date
            await ctx.send("Enter the event date:")
            date_message = await self.bot.wait_for("message", check=check, timeout=60)

            # Wait for the event time
            await ctx.send("Enter the event time:")
            time_message = await self.bot.wait_for("message", check=check, timeout=60)

            # Wait for the event description
            await ctx.send("Enter the event description:")
            description_message = await self.bot.wait_for("message", check=check, timeout=60)

            # Process the event information
            event_date = " 📅 " + date_message.content
            event_time = time_message.content
            event_description = description_message.content

            # Perform actions with the event information
            # e.g., store it in a database, send notifications, etc.

            # Add reaction buttons for user interaction
            await ctx.send("Do you want to attend this event?")
            role_message = await ctx.send(":shield: to Tank, :crossed_swords: for DPS, :deciduous_tree: for Healer.")

            # Add reaction buttons to the role_message
            await role_message.add_reaction(":shield:")
            await role_message.add_reaction(":crossed_swords:")
            await role_message.add_reaction(":deciduous_tree:")

            # Wait for user's reaction
            def reaction_check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in [":shield:", ":crossed_swords:",
                                                                      ":deciduous_tree:"]

            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=reaction_check, timeout=60)
                if str(reaction.emoji) == ":shield:":
                    await ctx.send("You have confirmed your role as tank.")
                else:
                    await ctx.send("")

            except asyncio.TimeoutError:
                await ctx.send("No reaction received. Event attendance not confirmed.")

            # Reply with a confirmation message
            await ctx.send("Event created successfully!")

        except asyncio.TimeoutError:
            await ctx.send("Event creation timed out.")

    bot = commands.Bot(command_prefix='!')

    bot.add_cog(Event(bot))
load_dotenv()

TOKEN = os.getenv('TOKEN')
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.add_cog(Event(bot))
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
