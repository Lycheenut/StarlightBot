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
