from . import ABCArg


class StaticArg(ABCArg):

    arg = None

    def __init__(self, arg: str):
        self.arg = arg

    def value(self) -> str:
        return self.arg

    def calc_value(self) -> str:
        return self.value()
