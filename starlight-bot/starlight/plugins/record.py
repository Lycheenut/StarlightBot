from nonebot import on_command, CommandSession
from ..database.mongo import collections
from ..utilities.constants import Constants
import time
import re

time.timezone = -43200


def _parse_args(args: str) -> list:
    stripped_args = args.strip()
    return stripped_args.split(' ')


def _quest_today(group_id: int) -> str:
    db = collections[str(group_id)]
    if not db:
        return ''

    today = time.strftime('%Y-%m-%d')
    records = db.find_record(date=today, contain_delay=True)
    record_str = ''
    i = 1
    for record in records:
        member_id = record['member_id']
        nickname = db.find_member(member_id=member_id)['nickname']
        item_str = str(i) + '. ' + record['date'] + ' ' + str(record['round']) + '周目 '
        item_str += str(record['boss']) + '王 ' + nickname + '佬 ' + str(record['score'])
        if record['delay']:
            item_str += '（补）'
        record_str += (item_str + '\n')
        i += 1
    if record_str == '':
        record_str = '今日尚无人出刀'

    return record_str


@on_command('help', aliases=('h', '帮助'))
async def show_help(session: CommandSession):
    await session.send(Constants.USAGE_MESSAGE)


@on_command('t', aliases=('today', '今日', '统计'))
async def quest_today(session: CommandSession):
    group_id = session.ctx['group_id']
    if not group_id:
        user_id = session.ctx['user_id']
    record_str = _quest_today(group_id)
    if not record_str:
        await session.send(Constants.NOT_IN_GUILD_ERROR_MESSAGE)
    else:
        await session.send(record_str.strip())


def _quest_rest(group_id: int) -> str:
    db = collections[str(group_id)]
    members = db.find_member()
    rest_list = ''
    delay_list = ''
    for member in members:
        member_id = member['member_id']
        today = time.strftime('%Y-%m-%d')
        records = db.find_record(date=today, member_id=member_id)
        times = len(records)
        if times < Constants.DAILY_MAX_TIME:
            rest_list += member['nickname'] + '佬剩余' + str(DAILY_MAX_TIME - times) + '次\n'
        delay = db.find_delay(member_id=member_id)
        for i in delay:
            delay_list += member['nickname'] + '佬有' + str(i['turns']) + '回合补偿刀\n'
    if rest_list == '':
        rest_list = '今日出刀已完成'
    return rest_list + delay_list


@on_command('r', aliases=('rest', '余刀', '剩刀'))
async def quest_rest(session: CommandSession):

    await session.send(''.strip())


@on_command('delay', aliases=('d', '补偿'))
async def do_delay(session: CommandSession):
    args = session.get('args')
    if not args:
        await session.send('请输入补偿刀伤害')
    else:
        score = args[0]
        no = 1
        if len(args) > 1:
            no = args[1]
        member_id = session.ctx['user_id'] * (10 ** (abs(no) - 1))
        delay = db.find_delay(member_id=member_id)
        if not delay:
            await session.send('您没有补偿刀')
        else:
            db.insert_record({
                "round": delay[0]['round'],
                "boss": delay[0]['boss'],
                "score": score,
                "delay": True,
                "member_id": member_id,
                "date": time.strftime('%Y-%m-%d')
            })
            db.remove_delay(member_id=member_id)
            await session.send('报刀成功')


@do_delay.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if re.match(r'[0-9]+( -[123])?', stripped_arg):
        args = []
        try:
            for arg in stripped_arg.split(' '):
                arg = int(arg)
                args.append(arg)
            session.state['args'] = args
        except ValueError:
            session.state['args'] = args
    else:
        session.state['args'] = []


@on_command('add', aliases=('a', '报刀'))
async def add_record(session: CommandSession):
    args = session.get('args')
    if not args:
        await session.send('请输入正确的出刀信息')
    else:
        no = 1
        if len(args) > 4:
            no = args[4]
        member_id = session.ctx['user_id'] * (10 ** (abs(no) - 1))
        if len(db.find_record(member_id=member_id)) >= 3:
            await session.send('今日您已经出完刀啦！大佬辛苦了！')
        else:
            if args[3] != 0:
                if db.find_delay(member_id):
                    await session.send('您还有未报的补偿刀，请检查后再报刀！')
                    return
                else:
                    db.insert_delay({
                        "round": args[0],
                        "boss": args[1],
                        "turns": args[3],
                        "member_id": member_id
                    })
            db.insert_record({
                "round": args[0],
                "boss": args[1],
                "score": args[2],
                "delay": False,
                "member_id": member_id,
                "date": time.strftime('%Y-%m-%d')
            })
            await session.send('报刀成功')


@add_record.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if re.match(r'[012]?[0-9]+ [1234] [0-9]+ [012345]( -[123])?', stripped_arg):
        args = []
        try:
            for arg in stripped_arg.split(' '):
                arg = int(arg)
                args.append(arg)
            session.state['args'] = args
        except ValueError:
            session.state['args'] = args
    else:
        session.state['args'] = []
