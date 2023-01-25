import re

from . import ABCArg
from domain import Dice


class DiceArg(ABCArg):

    REGEX = r"^(\d+)d(\d+)$"

    dice = None
    result = None

    def __init__(self, arg: str):

        match = re.search(self.REGEX, arg)
        if match:
            amount = int(match.groups()[0])
            size = int(match.groups()[1])
            self.dice = Dice(amount, size)
        else:
            raise Exception(f"Invalid DiceArg: {arg}.")

    def value(self) -> str:
        if self.result != None:
            return self.result

        dices = self.dice.roll()
        if len(dices) == 1:
            self.result = str(dices[0])
        else:
            self.result = str(dices)

        return self.result

    def calc_value(self) -> str:
        return self.value()
