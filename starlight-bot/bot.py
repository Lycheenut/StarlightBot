from os import path
import nonebot
import config
# from starlight.database.mongo import db


if __name__ == '__main__':
    nonebot.init(config)
    # nonebot.load_builtin_plugins()
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'starlight', 'plugins'),
        'starlight.plugins'
    )
    nonebot.run()

# if __name__ == '__main__':
#     db.insert_member({
#         "member_id": 81065449,
#         "nickname": "张"
#     })
#     db.insert_member({
#         "member_id": 1286804583,
#         "nickname": "苏大"
#     })
#     db.insert_member({
#         "member_id": 863506305,
#         "nickname": "lychee"
#     })
