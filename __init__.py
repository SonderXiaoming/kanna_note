import contextlib
import copy
import re

from loguru import logger
import nonebot
from zoneinfo import ZoneInfo
from .base import ServerType
from .download import update_pcr_database
from .util import (
    DEFAULT_GROUP_CONFIG,
    convert2gameid,
    format_remaining,
    get_chara,
    load_data,
    phase_dict,
    save_data,
)
import hoshino
from hoshino import Service, get_bot
from hoshino.typing import CQEvent, HoshinoBot
from .handle import (
    get_boss_max_time_return_line,
    get_chara_skill,
    get_chara_story,
    get_chara_unique_equip,
    get_clan_battle_info,
    get_enemy_id,
    get_enemy_skill,
    get_schedule,
    init,
    get_chara_introduce,
    get_expiring_events,
    send_calendar,
    update_group_schedule,
)
from itertools import product

help_ = """
[@bot简介环奈] 角色简介
[@bot技能环奈] 角色技能
[@bot专武环奈] 角色专武
[@bot羁绊环奈] 角色羁绊
[@botBOSS技能] BOSS技能 后面跟会战ID和阶段ID
* 例：@botBOSS技能1064d5
[公会战信息] 公会战信息
[公会战信息2] 公会战信息第2页
[日程] 活动日历
[日程提醒设置 关闭/08:00] 开启/关闭定时推送（管理员）
[日程提醒状态] 查看推送设置
[日程提醒到期提醒 开启/关闭] 开启/关闭活动结束提醒（管理员）
[满补线] 满补线查询，后面可以跟会战数字指定期数
* 可以加上"台"或"日"来查询台服或日服数据
* 例：@bot台专武情姐 （看专2）
* 前面#号表示查询ID
* 例：@bot简介#1701
* 例：@bot技能#1064d5 (1064为公会战ID，d5为阶段id)
* 例：日日程 （查询日服日程）
会战ID可以使用公会战信息查询
不写会自动查找角色存在的服务器
优先级 国服>台服>日服
""".strip()

sv = Service(
    "环奈笔记",
    help_=help_,
    bundle="pcr查询",
)

data_type = ("", "台", "日")
type_dict = {"": "cn", "台": "tw", "日": "jp"}
group_data = None

introduce_query = tuple(
    f"{type_}{command}" for type_, command in product(data_type, ("简介", "介绍"))
)
unique_query = tuple(
    f"{type_}{command}" for type_, command in product(data_type, ("专武",))
)
kizuna_query = tuple(
    f"{type_}{command}" for type_, command in product(data_type, ("羁绊",))
)
skill_query = tuple(
    f"{type_}{command}" for type_, command in product(data_type, ("技能",))
)

clan_battle_query = tuple(
    f"{type_}{command}信息"
    for type_, command in product(data_type, ("公会战", "公会", "会战"))
)

enemy_skill_query = tuple(
    f"{type_}{command}技能" for type_, command in product(data_type, ("BOSS", "boss"))
)

schedule_query = tuple(
    f"{type_}{command}"
    for type_, command in product(data_type, ("日历", "日程", "活动", "活动日历"))
)

schedule_remind_query = tuple(
    f"{type_}{command}"
    for type_, command in product(
        data_type, ("日程提醒设置", "活动提醒设置", "活动日历提醒设置")
    )
)
max_time_line_query = tuple(
    f"{type_}{command}" for type_, command in product(data_type, ("满补线",))
)


@sv.on_fullmatch("环奈笔记帮助")
async def help(bot: HoshinoBot, ev: CQEvent):
    await bot.send(ev, help_)


@sv.on_prefix(introduce_query, only_to_me=True)
async def introduce(bot: HoshinoBot, ev: CQEvent):
    name = ev.message.extract_plain_text().strip()
    if not name:
        await bot.send(ev, '请发送"简介"+别称，如"简介环奈“')
        return
    _id, msg = get_chara(name)
    if msg:
        await bot.send(ev, msg)
        return
    type_ = ""
    if "台" in ev.prefix:
        type_ = "tw"
    elif "日" in ev.prefix:
        type_ = "jp"
    await bot.send(ev, await get_chara_introduce(convert2gameid(_id), type_=type_))


@sv.on_prefix(unique_query, only_to_me=True)
async def unique(bot: HoshinoBot, ev: CQEvent):
    name = ev.message.extract_plain_text().strip()
    if not name:
        await bot.send(ev, '请发送"专武"+别称，如"专武环奈“')
        return
    _id, msg = get_chara(name)
    if msg:
        await bot.send(ev, msg)
        return
    type_ = ""
    if "台" in ev.prefix:
        type_ = "tw"
    elif "日" in ev.prefix:
        type_ = "jp"
    await bot.send(ev, await get_chara_unique_equip(convert2gameid(_id), type_=type_))


@sv.on_prefix(kizuna_query, only_to_me=True)
async def kizuna(bot: HoshinoBot, ev: CQEvent):
    name = ev.message.extract_plain_text().strip()
    if not name:
        await bot.send(ev, '请发送"羁绊"+别称，如"羁绊环奈“')
        return
    _id, msg = get_chara(name)
    if msg:
        await bot.send(ev, msg)
        return
    type_ = ""
    if "台" in ev.prefix:
        type_ = "tw"
    elif "日" in ev.prefix:
        type_ = "jp"
    await bot.send(ev, await get_chara_story(convert2gameid(_id), type_=type_))


@sv.on_prefix(skill_query, only_to_me=True)
async def skill(bot, ev: CQEvent):
    name = ev.message.extract_plain_text().strip()
    if not name:
        await bot.send(ev, '请发送"技能"+别称，如"技能环奈“')
        return
    _id, msg = get_chara(name)
    if msg:
        await bot.send(ev, msg)
        return
    type_ = ""
    if "台" in ev.prefix:
        type_ = "tw"
    elif "日" in ev.prefix:
        type_ = "jp"
    await bot.send(ev, await get_chara_skill(convert2gameid(_id), type_=type_))


@sv.on_prefix(enemy_skill_query, only_to_me=True)
async def enemy_skill(bot, ev: CQEvent):
    args = ev.message.extract_plain_text().strip()
    type_ = ""
    if "台" in ev.prefix:
        type_ = "tw"
    elif "日" in ev.prefix:
        type_ = "jp"
    if "#" in args:
        enemy_id = int(args[1:])
        _id = enemy_id
    else:
        matches = re.match(r"(\d+)([a-zA-Z])(\d+)", args)
        if not matches:
            await bot.send(ev, "请输入正确的格式,如1064d5")
            return

        _id, enemy_id = await get_enemy_id(
            int(matches[1]),
            phase_dict[matches[2].upper()],
            int(matches[3]),
            type_=type_,
        )  # enemy_id 是实际的敌人ID，_id 更像是种类。例如今年的金牛座和去年的金牛座种类一样，数值技能什么不同

    await bot.send(ev, await get_enemy_skill(_id, enemy_id=enemy_id, type_=type_))


@sv.on_prefix(clan_battle_query)
async def clan_battle(bot: HoshinoBot, ev: CQEvent):
    page: str = ev.message.extract_plain_text().strip()
    if not page:
        page = 1
    elif not page.isdigit():
        await bot.send(ev, "请输入正确页码")
        return
    else:
        page = int(page)
    type_ = ""
    if "台" in ev.prefix:
        type_ = "tw"
    elif "日" in ev.prefix:
        type_ = "jp"
    await bot.send(ev, await get_clan_battle_info(page, type_=type_))


@sv.on_fullmatch(schedule_query)
async def schedule(bot: HoshinoBot, ev: CQEvent):
    command = ev.prefix.replace("日历", "").replace("日程", "")
    type_ = ""
    if "台" in command:
        type_ = "tw"
    elif "日" in command:
        type_ = "jp"
    await bot.send(ev, await get_schedule(type_=type_))


@sv.on_prefix(max_time_line_query)
async def max_time_line(bot: HoshinoBot, ev: CQEvent):
    clan_id = ev.message.extract_plain_text().strip()
    type_ = ""
    if "台" in ev.prefix:
        type_ = "tw"
    elif "日" in ev.prefix:
        type_ = "jp"
    await bot.send(
        ev, await get_boss_max_time_return_line(type_=type_, clan_battle_id=clan_id)
    )


@sv.on_prefix(schedule_remind_query)
async def schedule_remind(bot, ev: CQEvent):
    if not hoshino.priv.check_priv(ev, hoshino.priv.ADMIN):
        await bot.send(ev, "权限不足")
        return
    command = ev.message.extract_plain_text().strip()
    type_ = ""
    prefix = ev.prefix.strip().replace("日历", "").replace("日程", "")
    if "台" in prefix:
        type_ = "tw"
    elif "日" in prefix:
        type_ = "jp"
    else:
        type_ = "cn"
    group_id = str(ev.group_id)
    config = group_data.get(group_id, copy.deepcopy(DEFAULT_GROUP_CONFIG))

    if not command:
        return
    elif command == "关闭":
        config["server_list"] = []
        group_data[str(ev.group_id)] = config
        save_data(group_data)
        with contextlib.suppress(Exception):
            nonebot.scheduler.remove_job(f"pcr_wiki_schedule_{group_id}")
        await bot.send(ev, "日程推送已关闭")
        return
    else:
        match = re.match(r"(\d{1,2}):(\d{1,2})", command)
        if not match:
            await bot.send(ev, "请输入正确的时间，例如: 日程提醒设置 08:00")
            return
        hour = int(match.group(1))
        minute = int(match.group(2))
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            await bot.send(ev, "请输入正确的时间，例如: 日程提醒设置 08:00")
            return
        config["hour"] = hour
        config["minute"] = minute
        if type_ not in config["server_list"]:
            config["server_list"].append(type_)
        group_data[str(ev.group_id)] = config
        save_data(group_data)

        nonebot.scheduler.add_job(
            send_calendar,
            "cron",
            args=(str(ev.group_id), group_data[str(ev.group_id)]),
            id=f"pcr_wiki_schedule_{str(ev.group_id)}",
            replace_existing=True,
            hour=hour,
            minute=minute,
            timezone=ZoneInfo("Asia/Shanghai"),
            misfire_grace_time=60,
            coalesce=True,
        )
        await bot.send(ev, f"日程推送时间已设置为: {hour}:{minute:02d}")


@sv.on_prefix("日程提醒到期提醒")
async def schedule_remind_expire(bot: HoshinoBot, ev: CQEvent):
    if not hoshino.priv.check_priv(ev, hoshino.priv.ADMIN):
        await bot.send(ev, "权限不足")
        return
    command = ev.message.extract_plain_text().strip()
    config = group_data.get(str(ev.group_id), copy.deepcopy(DEFAULT_GROUP_CONFIG))
    if not command:
        return
    elif command == "开启":
        config["expire_remind"] = True
        group_data[str(ev.group_id)] = config
        save_data(group_data)
        await bot.send(ev, "活动结束提醒已开启")
        return
    elif command == "关闭":
        config["expire_remind"] = False
        group_data[str(ev.group_id)] = config
        save_data(group_data)
        await bot.send(ev, "活动结束提醒已关闭")
        return
    else:
        await bot.send(ev, "请输入正确的指令，例如: 日程提醒到期提醒 开启/关闭")
        return


@sv.on_fullmatch("日程提醒状态")
async def schedule_remind_status(bot: HoshinoBot, ev: CQEvent):
    config = group_data.get(str(ev.group_id), DEFAULT_GROUP_CONFIG)
    servers = "、".join(ServerType.get(s).name for s in config["server_list"]) or "无"
    expire_status = "开启" if config.get("expire_remind") else "关闭"
    msg = (
        f"订阅区服: {servers}\n"
        f"推送时间: {config['hour']}:{config['minute']:02d}\n"
        f"活动结束提醒: {expire_status}"
    )
    await bot.send(ev, msg)


@sv.scheduled_job("cron", hour="11", minute="45", jitter=14)
@sv.on_fullmatch("更新wiki数据库")
async def update_data_base(bot=None, ev=None):
    await update_pcr_database()
    await init()
    if bot and ev:
        await bot.send(ev, "更新成功")


@sv.scheduled_job("cron", minute=0, hour="*")
async def check_expiring_events():
    server_cache = {}
    bot = get_bot()
    for group_id, config in group_data.items():
        if not config.get("expire_remind") or not config["server_list"]:
            continue
        try:
            lines = []
            for server in config["server_list"]:
                if server not in server_cache:
                    expiring = await get_expiring_events(type_=server)
                    server_cache[server] = [
                        f"[{ServerType.get(server).name}] {name}\n"
                        f"结束时间: {end_time}\n"
                        f"剩余: {format_remaining(remaining)}"
                        for name, end_time, remaining in expiring
                    ]
                lines.extend(server_cache[server])
            if not lines:
                continue
            await bot.send_group_msg(
                group_id=int(group_id),
                message="以下活动将在1小时内结束：\n" + "\n".join(lines),
            )
            logger.info(f"群{group_id}活动结束提醒已发送")
        except Exception:
            logger.exception(f"群{group_id}活动结束提醒失败")


@nonebot.on_startup
async def startup():
    global group_data
    group_data = load_data()
    update_group_schedule(group_data)
