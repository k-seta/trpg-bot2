import re


class CommandInterpreter:

    REGEX = r"^\.(\w+)([\s|\S]*)$"

    valid = False
    command = ""
    args = []

    def __init__(self, message):
        match = re.match(self.REGEX, message)
        if match:
            self.valid = True
            self.command = match.groups()[0]
            self.args = list(filter(None, match.groups()[1].split(" ")))

    def __str__(self):
        return f"CommandInterpreter: {vars(self)}"

    def invalid(self):
        return not self.valid

    def is_ping(self):
        return self.command == "ping"

    def is_dice(self):
        return self.command == "dice"

    def is_register(self):
        return self.command == "register"

    def is_status(self):
        return self.command == "status"
