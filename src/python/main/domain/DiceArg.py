import re

from . import ABCArg, Dice


class DiceArg(ABCArg):

    REGEX = r"^(\d+)d(\d+)$"

    dice = None

    def __init__(self, arg: str):

        match = re.search(self.REGEX, arg)
        if match:
            amount = int(match.groups()[0])
            size = int(match.groups()[1])
            self.dice = Dice(amount, size)
        else:
            raise Exception(f"Invalid DiceArg: {arg}.")

    def value(self) -> str:
        dices = self.dice.roll()
        if len(dices) == 1:
            return f"{dices[0]}"
        else:
            return f"{dices}"
