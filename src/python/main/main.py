import os
import logging
import traceback
import discord

from domain import CommandInterpreter
from usecase import CocUsecase
from repository import PlayerRepository

TOKEN = os.environ["DISCORD_BOT_TOKEN"]

logger = logging.getLogger("discord")
log_level = logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO"))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

repository = PlayerRepository()


@client.event
async def on_ready():
    logger.info(f"activated as {client.user}")


@client.event
async def on_message(message):

    if message.author.bot:
        return

    guild = message.guild.name
    channel = message.channel.name
    username = message.author.name

    try:
        interpreter = CommandInterpreter(message.content)
        logger.debug(interpreter)

        if interpreter.invalid():
            return

        if interpreter.is_ping():
            await message.channel.send("pong")

        usecase = CocUsecase(guild, channel, username, interpreter, repository)
        if interpreter.is_dice():
            await message.channel.send(
                f"{message.author.mention} がサイコロを振ったよ\n=> {usecase.dice_message()}"
            )

        if interpreter.is_register():
            await message.channel.send(
                f"{message.author.mention} がキャラシートを登録したよ\n=> {usecase.register_message()}"
            )

        if interpreter.is_status():
            await message.channel.send(
                f"{message.author.mention} のキャラシートだよ\n```{usecase.status_message()}```"
            )

    except Exception as e:
        await message.channel.send(f"何かエラーが起きたみたいだよ\n```{str(e)}```")
        traceback.print_exc()


client.run(TOKEN, log_level=log_level)
