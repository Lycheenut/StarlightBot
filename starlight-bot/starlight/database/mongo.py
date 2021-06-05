from typing import Optional

import pymongo
from .doc_types import Player, Guild, Record
from ..config import HOST, MONGO_PORT


class MongoStarlight:
    def __init__(self, url):
        self._client = pymongo.MongoClient(url)
        self._starlight = self._client['starlight']
        self._players = self._starlight['players']
        self._guilds = self._starlight['guilds']
        self._accounts = self._starlight['accounts']
        self._records = self._starlight['records']
        self._delays = self._starlight['delays']

    def add_player(self, player_id: int, nickname: str):
        return self._players.insert_one(Player(player_id, nickname).__dict__)

    def modify_player(self, player_id: int, nickname: str):
        return self._players.update_one({"player_id": player_id}, {"nickname": nickname})

    change_nickname = modify_player

    def remove_player(self, player_id: int):
        return self._players.delete_many({"player_id": player_id})

    def find_player(self, player_id: Optional[int]):
        if player_id:
            return self._players.find_one({"player_id": player_id})
        else:
            players = []
            for player in self._players.find():
                players.append(player)
            return players

    def add_record(self, game_id: int, record_time: str, round_no: int, boss_no: int, score: int):
        return self._records.insert_one(Record(game_id, record_time, round_no, boss_no, score).__dict__)

    def modify_record(self, record_filter: dict, update: dict):
        return self._records.update_one(record_filter, update)

    def remove_record(self, record_filter: dict):
        return self._records.delete_many(record_filter)

    def find_record(self, record_filter: dict):
        records = []
        for record in self._records.find(record_filter):
            records.append(record)
        return records

    def add_guild_member(self, game_id: int, guild_id: int):
        guild_filter = {"guild_id": guild_id}
        if self._guilds.count(guild_filter) == 0:
            self._guilds.insert_one(Guild(guild_id).__dict__)
        guild = self._guilds.find_one(guild_filter)
        guild['members'].append(game_id)
        return self._guilds.update_many(guild_filter, guild)

    def remove_guild_member(self, game_id: int):
        account = self._accounts.find_one({"game_id": game_id})
        if not account:
            return None
        guild_id = account['guild_id']
        guild = self._guilds.find_one({"guild_id": guild_id})
        members = guild['members'].remove(game_id)
        self._accounts.update_one({"game_id": game_id}, {"guild_id": 0})
        return self._guilds.update_one({"guild_id": guild_id}, {"members": members})


client_url = 'mongodb://' + HOST + ':' + str(MONGO_PORT) + '/'
db = MongoStarlight(url=client_url)
collections = {}
