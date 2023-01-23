from . import CocPlayer


class PlayerRepository:

    db = []

    def __init__(self):
        self.db = []

    def get(self, guild, channel, username):
        for player in self.db:
            if (
                player.guild == guild
                and player.channel == channel
                and player.user == username
            ):
                return player
        return None

    def insert(self, guild, channel, username, url):
        player = self.get(guild, channel, username)
        if player == None:
            new_player = CocPlayer(guild, channel, username, url=url)
            self.db.append(new_player)
        elif player.url != url:
            player.change_url(url)
        else:
            return

    def delete_all(self):
        self.db = []
