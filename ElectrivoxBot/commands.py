import discord
import asyncio
from discord.ext import commands

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create_event(self, ctx):
        # Prompt the user for event details
        await ctx.send("Please provide the event details.")

        # Wait for the user's response
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

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

def setup(bot):
    bot.add_cog(Event(bot))
