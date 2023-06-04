import asyncio
import uuid
import pymongo
from datetime import timedelta
from ElectrivoxBot.bot import bot
from discord.ext import commands


# Set up the MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
db = client["Electrivox"]  # Replace with your database name

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
                # Gather input from the user
                event_name = input("Enter the event name: ")
                event_date = input("Enter the event date: ")
                event_description = input("Enter the event description: ")

                # Generate a unique event ID
                event_id = str(uuid.uuid4())

                # Store event details in a database
                # Assuming you have a database connection established
                db.insert_event(event_id, event_name, event_date, event_description)

                # Send event notifications to users
                users = db.fetch_subscribed_users()  # Fetch users who want event notifications
                for user in users:
                    user.send_message(f"New event created: {event_name} on {event_date}")

                # Set up event reminders
                reminder_time = event_date - timedelta(hours=1)  # Adjust reminder time as needed
                asyncio.create_task(self.send_reminder(event_id, reminder_time))

                # Send a confirmation message
                await ctx.send("Event created!")

            async def send_reminder(event_id, reminder_time):
                await asyncio.sleep(reminder_time.total_seconds())
                event = db.fetch_event(event_id)
                if event:
                    users = db.fetch_subscribed_users()  # Fetch users who want reminders
                    for user in users:
                        user.send_message(f"Reminder: Upcoming event {event.name} in 1 hour")


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
