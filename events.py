import discord
from bot import bot
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user.name}')

async def on_message(bot, message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Process commands
    await bot.process_commands(message)
