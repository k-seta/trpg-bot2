import os
import logging
import firebase_admin
from firebase_admin import credentials

from . import CocPlayer

logger = logging.getLogger("discord")

class PlayerRepository:

    db = []

    def __init__(self):
        self.db = []
        self.__init_db_client()

    def __init_db_client(self):
        if os.environ.get("FIRESTORE_EMULATOR_HOST") != None:
            # local環境
            cred = credentials.Certificate("firebase.local.json")
            if (not len(firebase_admin._apps)):
                firebase_admin.initialize_app(cred)
            logger.debug("Finished firebase_admin.initialize_app for Local env")
        else:
            # prd環境
            # TODO: credentialの読み込みとinitialize
            logger.debug("Skip firebase_admin.initialize_app for Prod env")
            return

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

    def delete(self, guild, channel, username):
        self.db = [
            player
            for player in self.db
            if player.guild != guild
            or player.channel != channel
            or player.user != username
        ]

    def delete_all(self):
        self.db = []
