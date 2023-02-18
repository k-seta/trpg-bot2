import os
import logging
import textwrap
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
document = """
    .help
    ヘルプドキュメントを表示します。

    .ping
    bot との疎通確認を行います。

    .dice [個数]d[サイコロの面数]
    サイコロを振ります。定数も指定できます。
    e.g.) ".dice 1d100", ".dice 2d6 + 6"

    .register [キャラクターシートのURL]
    キャラクターシートのURLを登録します。
    キャラクターシートのデータはチャンネル毎に管理されます。
    e.g.) ".register https://charasheet.vampire-blood.net/3070216"

    .sync
    キャラクターシートのデータ URL 先のデータと同期します。

    .players
    その discord サーバーに登録されているキャラクターシートの一覧を表示します。

    ***
    以下のコマンドは .register で、https://charasheet.vampire-blood.net のキャラクターシートを登録したときのみ利用できます。
    以下のコマンドを使いたい場合は、キャラクターシート作成時に「自分以外から隠す」のチェックは外して保存するようにしてください。
    ***

    .dice [個数]d[サイコロの面数] < [能力値・技能]
    サイコロを振ります。
    同時に、キャラクターシートの最新パラメータを取得して、右側に表示します。
    e.g.) ".dice 1d100 < SAN", ".dice 1d100 < 目星"

    .status
    登録されているキャラクターシートの最新情報を取得して表示します。

    ***
    管理者専用コマンド
    ***

    .reset
    キャラクターシートの DB をリセットします

"""


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

        if interpreter.is_help():
            await message.channel.send(f"```{textwrap.dedent(document)[1:-1]}```")

        usecase = CocUsecase(guild, channel, username, interpreter, repository)
        if interpreter.is_dice():
            await message.channel.send(
                f"{message.author.mention} がサイコロを振ったよ\n=> {usecase.dice_message()}"
            )

        if interpreter.is_register():
            await message.channel.send(
                f"{message.author.mention} がキャラシートを登録したよ\n=> {usecase.register_message()}"
            )

        if interpreter.is_sync():
            await message.channel.send(
                f"{message.author.mention} がキャラシートを更新したよ\n=> {usecase.sync_message()}"
            )

        if interpreter.is_status():
            await message.channel.send(
                f"{message.author.mention} のキャラシートだよ\n```{usecase.status_message()}```"
            )

        if interpreter.is_players():
            await message.channel.send(
                f"{guild} のキャラシート一覧だよ\n```{usecase.players_message()}```"
            )

        # 管理者専用コマンド
        if message.author.guild_permissions.administrator:
            if interpreter.is_reset():
                repository.delete_all()
                await message.channel.send("管理者権限で DB がリセットされました")

    except Exception as e:
        await message.channel.send(f"何かエラーが起きたみたいだよ\n```{str(e)}```")
        traceback.print_exc()


client.run(TOKEN, log_level=log_level)
