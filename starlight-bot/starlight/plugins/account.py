from nonebot import on_command, CommandSession
from ..utilities.constants import Constants
import re


def _bind(group_id, game_id, user_id):
    return


@on_command('b', aliases=('bind', '绑定'))
async def bind(session: CommandSession):
    group_id = session.ctx['group_id']
    user_id = session.ctx['user_id']
    try:
        game_id = session.state['game_id']
    except AttributeError:
        await session.send(Constants.ARGS_NOT_MATCH_ERROR_MSG)
        return
    if _bind(group_id, game_id, user_id) == 0:
        await session.send(Constants.BIND_ACCOUNT_SUCCESS_MSG)


@bind.args_parser
async def _(session: CommandSession):
    stripped_arg_text = session.current_arg_text.strip()
    if re.match(r'[0-9]{10}', stripped_arg_text):
        session.state['game_id'] = stripped_arg_text
