import os
import logging
import traceback
import discord

from domain import CommandInterpreter, Dice

TOKEN = os.environ["DISCORD_BOT_TOKEN"]

logger = logging.getLogger("discord")
log_level = logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO"))

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

    try:
        interpreter = CommandInterpreter(message.content)
        logger.debug(interpreter)

        if interpreter.invalid():
            return

        if interpreter.is_ping():
            await message.channel.send("pong")

        if interpreter.is_dice():
            dice = Dice(interpreter.args[0])
            await message.channel.send(
                f"{message.author.mention} がサイコロを振ったよ\n=> {dice.roll()}"
            )

    except Exception as e:
        await message.channel.send(f"何かエラーが起きたみたいだよ\n```{str(e)}```")
        traceback.print_exc()


client.run(TOKEN, log_level=log_level)
