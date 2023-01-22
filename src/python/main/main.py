import os
import logging
import discord

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

    if message.content.startswith(".ping"):
        await message.channel.send("pong")


client.run(TOKEN)
