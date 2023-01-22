from domain import CommandInterpreter
from .arg import DiceArg, PlayerArg, StaticArg
from player import CocPlayer


class CocUsecase:

    interpreter = None
    player = None

    def __init__(self, interpreter: CommandInterpreter, player: CocPlayer):
        self.interpreter = interpreter
        self.player = player

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
                player_arg = PlayerArg(arg, self.player)
            except Exception as e:
                pass
            else:
                clauses.append(player_arg)
                continue

            # 全てに該当しなかった arg はそのまま返す
            clauses.append(StaticArg(arg))

        return " ".join([clause.value() for clause in clauses])
