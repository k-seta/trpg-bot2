import re
import random


class Dice:

    amout = 0
    size = 0

    def __init__(self, amount, size):
        if amount > 0 and size > 0:
            self.amount = amount
            self.size = size
        else:
            raise Exception(f"Invalid Dice Parameters: {amount}, {size}.")

    def __str__(self):
        return f"Dice: {vars(self)}"

    def roll(self):
        return [random.randint(1, self.size) for i in range(self.amount)]
