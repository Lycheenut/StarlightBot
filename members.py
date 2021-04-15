import pymongo


client = pymongo.MongoClient('mongodb://localhost:27017/')
starlight = client['starlight']
members = starlight['members']

ms = [
    {
        "member_id": 1021203743,
        "nickname": "呆毛"
    },
    {
        "member_id": 563421852,
        "nickname": "点"
    },
    {
        "member_id": 602479811,
        "nickname": "海豹"
    },
    {
        "member_id": 359489244,
        "nickname": "慕水金山"
    },
    {
        "member_id": 550344992,
        "nickname": "tutti"
    },
    {
        "member_id": 862418090,
        "nickname": "喜喜"
    },
    {
        "member_id": 512879305,
        "nickname": "13"
    },
    {
        "member_id": 863506305,
        "nickname": "lychee"
    }
]

for member in ms:
    members.insert_one(member)
