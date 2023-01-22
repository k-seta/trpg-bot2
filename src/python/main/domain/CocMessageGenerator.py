from domain import CommandInterpreter, DiceArg, StaticArg


class CocMessageGenerator:

    interpreter = None

    def __init__(self, interpreter: CommandInterpreter):
        self.interpreter = interpreter

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

            # 全てに該当しなかった arg はそのまま返す
            clauses.append(StaticArg(arg))

        return " ".join([clause.value() for clause in clauses])
