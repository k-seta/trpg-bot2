import re
import random
import textwrap

from . import CommandInterpreter


class Dice:

    amout = 0
    size = 0

    def __init__(self, param: str):

        match = re.search(r"^(\d+)d(\d+)$", param)
        if match:
            self.amount = int(match.groups()[0])
            self.size = int(match.groups()[1])
        else:
            raise Exception("Invalid Dice Parameters.")

    def __str__(self):
        s = f"""
            dice: {self.amount}d{self.size}
        """
        return textwrap.dedent(s)[1:-1]

    def roll(self):
        return [random.randint(1, self.size) for i in range(self.amount)]
