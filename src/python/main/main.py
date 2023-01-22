import os
import logging
import discord

from domain import CommandInterpreter

TOKEN = os.environ["DISCORD_BOT_TOKEN"]

logger = logging.getLogger("discord")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    logger.info(f"activated as {client.user}")


@client.event
async def on_message(message):

    if message.author.bot:
        return

    interpreter = CommandInterpreter(message.content)
    print(interpreter)
    if interpreter.invalid():
        return

    if interpreter.is_ping():
        await message.channel.send("pong")


client.run(TOKEN)
