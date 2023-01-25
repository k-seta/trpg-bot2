from . import ABCArg
from repository import CocPlayer


class PlayerArg(ABCArg):

    param_key = ""
    param_value = ""

    def __init__(self, arg: str, player: CocPlayer):
        result = player.get(arg)
        if len(result) > 0:
            self.param_key = arg
            self.param_value = result
        else:
            raise Exception(f"Invalid PlayerParameter Key: {self.arg}.")

    def value(self) -> str:
        return f"{self.param_key} ({self.param_value})"

    def calc_value(self) -> str:
        return self.param_value
