import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def create_event(ctx):
    # Prompt the user for event details
    await ctx.send("Please provide the event details.")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        # Wait for the user to provide the event details
        event_details_msg = await bot.wait_for('message', check=check, timeout=60)

        # Process the event details
        event_details = event_details_msg.content

        # Prompt the user for role selection
        await ctx.send("Please select the roles for the event. React to this message with the desired role emojis.")

        # Define the roles and corresponding emojis
        roles = {
            'Role 1': '🛡️',
            'Role 2': '⚔️',
            'Role 3': '🌳'
        }

        # Add the role emojis as reactions to the message
        for emoji in roles.values():
            await ctx.message.add_reaction(emoji)

        # Function to check if the reaction is valid
        def reaction_check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in roles.values()

        # Wait for the user to react with a valid role emoji
        reaction, _ = await bot.wait_for('reaction_add', check=reaction_check, timeout=1800)

        # Get the selected role based on the reaction emoji
        selected_role = next(role for role, emoji in roles.items() if emoji == str(reaction.emoji))

        # Prompt the user to pick a date and time
        await ctx.send("Please pick a date and time for the event.")

        def date_check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        date_message = await bot.wait_for('message', check=date_check, timeout=300)
        event_date = date_message.content

        # Example: Save the event details, selected role, and event date to a database or perform other actions

        await ctx.send(f"Event created with details: {event_details}. Selected role: {selected_role}. Event date: "
                       f"{event_date}")

    except asyncio.TimeoutError:
        await ctx.send("Event creation timed out. Please try again.")

def setup(bot):
    bot.add_command(create_event)
