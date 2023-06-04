from ElectrivoxBot.bot import bot
from discord.ext import commands

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create_event(self, ctx):
        from discord.ext import commands

        class Event(commands.Cog):
            def __init__(self, bot):
                self.bot = bot

            @commands.command()
            async def create_event(self, ctx):
                # Prompt the user for event details
                await ctx.send("Please provide the event date:")
                date_msg = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
                event_date = date_msg.content

                await ctx.send("Please provide the event time:")
                time_msg = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
                event_time = time_msg.content

                await ctx.send("Please provide a description for the event:")
                description_msg = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
                event_description = description_msg.content

                # Create the event message with the collected details
                event_message = f"**Event Details:**\nDate: {event_date}\nTime: {event_time}\nDescription: " \
                                f"{event_description}"

                # Send the event message and add reaction buttons
                event_msg = await ctx.send(event_message)
                await event_msg.add_reaction(':shield:')  # Tank
                await event_msg.add_reaction(':crossed_swords:')  # DPS
                await event_msg.add_reaction(':deciduous_tree:') # Healer

                await ctx.send("Event created successfully!")

        def setup(bot):
            bot.add_cog(Event(bot))


def setup(bot):
    bot.add_cog(Event(bot))


async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user.name}')

async def on_message(bot, message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Process commands
    await bot.process_commands(message)
