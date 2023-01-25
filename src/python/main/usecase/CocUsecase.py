from domain import CommandInterpreter
from .arg import DiceArg, PlayerArg, StaticArg
from repository import PlayerRepository


class CocUsecase:

    guild = None
    channel = None
    username = None
    interpreter = None
    repository = None

    def __init__(
        self,
        guild: str,
        channel: str,
        username: str,
        interpreter: CommandInterpreter,
        repository: PlayerRepository,
    ):
        self.guild = guild
        self.channel = channel
        self.username = username
        self.interpreter = interpreter
        self.repository = repository

    def dice_message(self):
        clauses = []
        for arg in self.interpreter.args:
            # dice_arg の作成を試みる
            try:
                dice_arg = DiceArg(arg)
            except Exception as e:
                pass
            else:
                clauses.append(dice_arg)
                continue

            # player_arg の作成を試みる
            try:
                player = self.repository.get(self.guild, self.channel, self.username)
                player_arg = PlayerArg(arg, player)
            except Exception as e:
                pass
            else:
                clauses.append(player_arg)
                continue

            # 全てに該当しなかった arg はそのまま返す
            clauses.append(StaticArg(arg))

        return " ".join([clause.value() for clause in clauses])

    def register_message(self):
        url = self.interpreter.args[0]
        self.repository.insert(self.guild, self.channel, self.username, url)
        return url

    def status_message(self):
        player = self.repository.get(self.guild, self.channel, self.username)
        return player.print()
