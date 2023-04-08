import os
import logging
import firebase_admin
from firebase_admin import credentials, firestore

from . import CocPlayer

logger = logging.getLogger("discord")

class PlayerRepository:
    __guilds_key = u'guilds'
    __channels_key = u'channels'
    __players_key = u'players'

    db = []
    firestore_client = None

    def __init__(self):
        self.db = []
        self.firestore_client = None
        self.__init_db_client()

    def __init_db_client(self):
        if os.environ.get("FIRESTORE_EMULATOR_HOST") != None:
            # local環境
            cred = credentials.Certificate("firebase.local.json")
            if (not len(firebase_admin._apps)):
                firebase_admin.initialize_app(cred)
            logger.info("Finished firebase_admin.initialize_app for Local env")
            self.firestore_client = firestore.client()
        else:
            # prd環境
            # TODO: credentialの読み込みとinitialize
            logger.info("Skip firebase_admin.initialize_app for Prod env")
            return

    def __get_document_ref(self, guild, channel, player):
        return self.firestore_client\
        .collection(self.__guilds_key).document(guild)\
        .collection(self.__channels_key).document(channel)\
        .collection(self.__players_key).document(player)

    def get(self, guild, channel, username):
        if self.firestore_client == None:
            for player in self.db:
                if (
                    player.guild == guild
                    and player.channel == channel
                    and player.user == username
                ):
                    return player
            return None
        else:
            ref = self.__get_document_ref(guild, channel, username)
            doc = ref.get()
            if doc.exists:
                url = doc.to_dict()["url"]
                return CocPlayer(guild, channel, username, url=url)
            else:
                return None

    def insert(self, guild, channel, username, url):
        if self.firestore_client == None:
            player = self.get(guild, channel, username)
            if player == None:
                new_player = CocPlayer(guild, channel, username, url=url)
                self.db.append(new_player)
            elif player.url != url:
                player.change_url(url)
            else:
                return
        else:
            ref = self.__get_document_ref(guild, channel, username)
            ref.set({
                u'username': username,
                u'url': url,
                u'type': u'coc',
            })
            return

    def delete(self, guild, channel, username):
        if self.firestore_client == None:
            self.db = [
                player
                for player in self.db
                if player.guild != guild
                or player.channel != channel
                or player.user != username
            ]
        else:
            ref = self.__get_document_ref(guild, channel, username)
            ref.delete()

    def delete_all(self):
        if self.firestore_client == None:
            self.db = []
        else:
            for guild in self.firestore_client.collection(self.__guilds_key).list_documents():
                for channel in guild.collection(self.__channels_key).list_documents():
                    for player in channel.collection(self.__players_key).list_documents():
                        ty = player.get().to_dict()[u'type']
                        if ty == u'coc':
                            player.delete()
