import re
import textwrap


class CommandInterpreter:

    REGEX = r"^.(\w+)([\s|\S]*)$"

    valid = False
    command = ""
    args = []

    def __init__(self, message):
        match = re.match(self.REGEX, message)
        if match:
            groups = match.groups()
            self.valid = True
            self.command = groups[0]
            self.args = list(filter(None, groups[1].split(" ")))

    def __str__(self):
        s = f"""
            valid: {self.valid}
            command: {self.command}
            args: {self.args}
        """
        return textwrap.dedent(s)[1:-1]

    def invalid(self):
        return not self.valid

    def is_ping(self):
        return self.command == "ping"

    def is_dice(self):
        return self.command == "dice"
