class Player:
    def __init__(self, player_id: int, nickname: str):
        self.player_id = player_id
        self.nickname = nickname


class Account:
    def __init__(self, player_id: int, guild_id: int, game_id: int):
        self.player_id = player_id
        self.guild_id = guild_id
        self.game_id = game_id
        self.log_state = False


class Guild:
    def __init__(self, guild_id: int):
        self.guild_id = guild_id
        self.members = []


class Record:
    def __init__(self, game_id: int, record_time: str, round_no: int, boss_no: int, score: int):
        self.game_id = game_id
        self.record_time = record_time
        self.round = round_no
        self.boss = boss_no
        self.score = score


class Delay:
    def __init__(self, game_id: int, round_n: int):
        self.game_id = game_id
        self.round = round_n
