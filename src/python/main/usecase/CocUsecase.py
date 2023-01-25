from domain import CommandInterpreter
from .arg import DiceArg, PlayerArg, StaticArg
from repository import PlayerRepository


class CocUsecase:

    interpreter = None
    repository = None

    def __init__(self, interpreter: CommandInterpreter, repository: PlayerRepository):
        self.interpreter = interpreter
        self.repository = repository

    def dice_message(self, guild, channel, username):
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
                player = self.repository.get(guild, channel, username)
                player_arg = PlayerArg(arg, player)
            except Exception as e:
                pass
            else:
                clauses.append(player_arg)
                continue

            # 全てに該当しなかった arg はそのまま返す
            clauses.append(StaticArg(arg))

        return " ".join([clause.value() for clause in clauses])

    def register_message(self, guild, channel, username):
        url = self.interpreter.args[0]
        self.repository.insert(guild, channel, username, url)
        return url

    def status_message(self, guild, channel, username):
        player = self.repository.get(guild, channel, username)
        return player.print()
