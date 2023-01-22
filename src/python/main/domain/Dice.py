import re
import random


class Dice:

    amout = 0
    size = 0

    def __init__(self, param: str):

        match = re.search(r"^(\d+)d(\d+)$", param)
        if match:
            self.amount = int(match.groups()[0])
            self.size = int(match.groups()[1])
        else:
            raise Exception(f"Invalid Dice Parameters: {param}.")

    def __str__(self):
        return f"Dice: {vars(self)}"

    def roll(self):
        return [random.randint(1, self.size) for i in range(self.amount)]
