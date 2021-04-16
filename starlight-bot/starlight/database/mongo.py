import pymongo


class MongoStarlight:
    def __init__(self):
        self._client = pymongo.MongoClient('mongodb://localhost:27017/')
        self._starlight = self._client['starlight']
        self._records = self._starlight['records']
        self._members = self._starlight['members']
        self._delay = self._starlight['delay']

    def insert_record(self, record):
        x = self._records.insert_one(record)
        return x.inserted_id

    def insert_member(self, member):
        x = self._members.insert_one(member)
        return x.inserted_id

    def insert_delay(self, delay):
        x = self._delay.insert_one(delay)
        return x.inserted_id

    def find_record(self, date=None, member_id=None, contain_delay=False):
        find_filter = {}
        if date:
            find_filter['date'] = date
        if member_id:
            find_filter['member_id'] = member_id
        if not contain_delay:
            find_filter['delay'] = False

        y = self._records.find(find_filter)
        x = []
        for i in y:
            x.append(i)
        return x

    def find_member(self, member_id=None):
        if member_id:
            x = self._members.find({"member_id": member_id})[0]
        else:
            x = self._members.find()
        return x

    def find_delay(self, member_id=None):
        x = []
        if member_id:
            y = self._delay.find({"member_id": member_id})
        else:
            y = self._delay.find()
        for i in y:
            x.append(i)
        return x

    def remove_delay(self, member_id=None):
        if member_id:
            x = self._delay.delete_many({"member_id": member_id})
        else:
            x = self._delay.delete_many()
        return x


db = MongoStarlight()
