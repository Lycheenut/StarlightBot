import json

import requests
from nonebot import on_command, CommandSession

api_endpoint = "https://karth.top/api/dress"
attributes = ["无", "花", "风", "雪", "月", "宙", "云", "梦"]
roles = {
    "front": "前排",
    "middle": "中排",
    "back": "后排"
}
characters = [
    [],
    ["", "", "", "", "", "", "", "", "", "花柳香子"],
    ["", "", "", "", "", ""],
    ["", "", "", "", "", ""],
    ["", "", "", "", "", ""],
    ["", "", "", ""]
]


def get_chara(chara_id: int):
    school = int(chara_id / 100)
    chara = chara_id % 100
    return characters[school][chara]


def parse_stat(stats: dict) -> str:
    total = stats["total"]
    hp = stats["hp"]
    atk = stats["atk"]
    pdef = stats["pdef"]
    agi = stats["agi"]
    mdef = stats["mdef"]
    return f"战力: {total}\tHP:{hp}\n攻击: {atk}\t通常防御力:{pdef}\n敏捷: {agi}\t特殊防御力:{mdef}\n"


def parse_act(act: dict, act_num: str) -> str:
    cost = act["normalSkill"]["cost"]
    name = act["normalSkill"]["name"]["ja"]
    description = act["normalSkill"]["description"]["ja"]
    skill_info = act["normalSkill"]["skillInfo"]
    skill_cycle = act["normalSkill"]["skillCycle"]
    return f"ACT {act_num} {name} COST{cost}\n{description}\n{skill_info}\n{skill_cycle}"


def parse_skill(skill: dict, skill_num: str) -> str:
    return skill["info"]["ja"]


def parse_many(obj: dict, parse_func) -> str:
    ret = ""
    i = 1
    for j in obj:
        ret += (parse_func(j, str(i)) + "\n")
        i += 1
    return ret


def parse_info(info: dict) -> str:
    _basic_info = info["basicInfo"]

    name = _basic_info["name"]
    chara_id = _basic_info["character"]
    chara = get_chara(chara_id)
    _base = _basic_info["base"]

    attribute = attributes[_base["attribute"]]
    role = roles[_base["roleIndex"]["role"]]

    stat = parse_stat(info["stat"])

    acts = parse_many(info["act"], parse_act)
    skills = parse_many(info["skills"], parse_skill)
    us = info["groupSkills"]["unitSkill"]["info"]
    climax = parse_act(info["groupSkills"]["climaxACT"], " climax") + "\n"

    return f"{name} {chara}\n{attribute} {role}\n{stat}{acts}{climax}{skills}{us}"


@on_command("a")
async def quest_all(session: CommandSession):
    with open("../utilities/aliases.json") as aliases_file:
        aliases = json.load(aliases_file)
    # assert type(aliases) == list
    try:
        dress_id = aliases[session.state["keyword"]]
        url = api_endpoint + "/" + str(dress_id) + ".json"
        response = requests.get(url).text
        info = json.loads(response)
        contents = parse_info(info)
    except IndexError:
        contents = "未找到"
    await session.send(contents)
