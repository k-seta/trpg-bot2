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
                if arg in ["SAN"]:
                    # 不便なので、SAN の場合のみ自動でキャラシートを更新する
                    player = self.repository.get(self.guild, self.channel, self.username)
                    self.repository.delete(player.guild, player.channel, player.user)
                    self.repository.insert(player.guild, player.channel, player.user, player.url)
                player = self.repository.get(self.guild, self.channel, self.username)
                player_arg = PlayerArg(arg, player)
            except Exception as e:
                pass
            else:
                clauses.append(player_arg)
                continue

            # 全てに該当しなかった arg はそのまま返す
            clauses.append(StaticArg(arg))

        base_message = " ".join([clause.value() for clause in clauses])
        calc_clauses = [clause.calc_value() for clause in clauses]

        if len(calc_clauses) > 1 and all(
            [
                (clause.isdecimal() or clause in ["+", "-", "*", ">", "<"])
                for clause in calc_clauses
            ]
        ):
            formula = " ".join([clause for clause in calc_clauses])
            calc_result = eval(formula)
            return f"{base_message}\n=> {calc_result}"
        else:
            return base_message

    def register_message(self):
        url = self.interpreter.args[0]
        self.repository.insert(self.guild, self.channel, self.username, url)
        return url

    def sync_message(self):
        player = self.repository.get(self.guild, self.channel, self.username)
        self.repository.delete(player.guild, player.channel, player.user)
        self.repository.insert(player.guild, player.channel, player.user, player.url)
        return player.url

    def status_message(self):
        player = self.repository.get(self.guild, self.channel, self.username)
        if player != None:
            return player.print()
        else:
            return "キャラクターシートが登録されていません。\n'.register <url>' で登録してください。"

    def players_message(self):
        message = ""
        for player in self.repository.db:
            if player.guild == self.guild:
                message += f"{player.user}#{player.channel}: {player.url}\n"
        if len(message) > 0:
            return message
        else:
            return "キャラクターシートの登録件数は0件です。"
