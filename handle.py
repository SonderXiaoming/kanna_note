from datetime import datetime
from functools import wraps

import traceback
from typing import DefaultDict, Dict, List, Union

from loguru import logger

from .draw.draw_max_boss_time_return import draw_max_boss_time_return


from .draw.draw_event import (
    draw_birthday,
    draw_clan_battle_event,
    draw_free_gacha_event,
    draw_gacha_event,
    draw_story_event,
    drwa_calendar_event,
)

from .draw.draw_clan_battle_info import draw_clan_info
from .draw.draw_enemy_introduce import draw_enemy_introduce
from .draw.draw_unit_icon import draw_char_icon, draw_enemy_icon

from .draw.draw_unit_unique_equipment import (
    draw_unique_equipment,
)

from .draw.util import merge_pic

from .table import UnitSkillData

from .base import GameSetting

from .model import (
    BirthdayData,
    CalendarEvent,
    CampaignFreegachaData,
    CharaStoryStatusData,
    ClanBattleData,
    EventData,
    GachaHistoryData,
    UniqueEquipInfo,
    UnitInfo,
)
from .database import PCRDatabase, cn_data, jp_data, tw_data
from nonebot import on_startup
from .util import (
    cal_damage_by_max_time_return,
    convert2simplified,
    is_coming_soon,
    is_in_progress,
    pic2cqcode,
)
from .draw.draw_fullcard import draw_fullcard
from .skill_text_handle import get_skill_ids, get_skill_level
from .draw.draw_introduce import draw_introduce
from .draw.draw_story import draw_story
from .draw.draw_skill import draw_all_skill, draw_pattern

database_dict = {"cn": cn_data, "jp": jp_data, "tw": tw_data}


@on_startup
async def init():
    try:
        for data in database_dict.values():
            await data.init()
    except Exception as e:
        traceback.print_exc()
        logger.warning(f"初始化失败: {e}")


def judge_db_by_id(id_):
    return next(
        (
            type
            for type in ("cn", "tw", "jp")
            if id_ in database_dict[type].all_chaeacters
        ),
        None,
    )


def get_db_by_type(type):
    if type == "cn":
        return cn_data
    elif type == "tw":
        return tw_data
    elif type == "jp":
        return jp_data
    else:
        raise ValueError(f"无效的type: {type}")


def fetch_chara_data(func):
    """装饰器：解析 id_ 为 type_，并获取数据库数据"""

    @wraps(func)
    async def wrapper(id_, *args, type_=None, **kwargs):
        if not type_:
            type_ = judge_db_by_id(id_)
        if not type_:
            return f"没有查询到id为{id_}的wiki数据"
        data = get_db_by_type(type_)
        if not data:
            return f"无法获取 {type_} 类型的数据"

        return await func(
            id_, *args, type_=type_, data=data, **kwargs
        )  # 传递解析后的参数

    return wrapper


def judge_platform(func):
    """装饰器：解析 id_ 为 type_，并获取数据库数据"""

    @wraps(func)
    async def wrapper(*args, type_=None, **kwargs):
        if not type_:
            type_ = "cn"
        data = get_db_by_type(type_)
        if not data:
            return f"无法获取 {type_} 类型的数据"

        return await func(*args, type_=type_, data=data, **kwargs)  # 传递解析后的参数

    return wrapper


@fetch_chara_data
async def get_chara_introduce(id_: int, type_: str = None, data: PCRDatabase = None):
    info: UnitInfo = await data.get_unit_info_query(id_)
    unique_num = 0
    if await data.get_unique_equip_info(id_, slot=2):
        unique_num = 2
    elif await data.get_unique_equip_info(id_, slot=1):
        unique_num = 1

    # info = convert2simplified(info)
    if type_ == "tw":
        info = convert2simplified(info)
    try:
        fullcard = await draw_fullcard(info, unique_num)
        introduce = await draw_introduce(info)
        return f"{pic2cqcode(merge_pic((fullcard, introduce)))}\n"
    except Exception as e:
        traceback.print_exc()
        return f"{e}\n{pic2cqcode(await draw_introduce(info))}\n"


@fetch_chara_data
async def get_chara_unique_equip(
    id_: int,
    level1: int = None,
    level2: int = None,
    type_: str = None,
    data: PCRDatabase = None,
):
    if not level1:
        level1 = data.max_unique_equip_lv[0]
    if not level2:
        level2 = data.max_unique_equip_lv[1]
    orginal_level1 = level1
    orginal_level2 = level2

    unit_info = await data.get_unit_info_query(id_)
    skill_info = await data.get_unit_skill(unit_info.cutin1_star6 or unit_info.unit_id)

    skills = {
        "normal": [],
        "sp": [],
    }
    if level1 <= GameSetting.tp_limit_level.value:
        equip_list = [
            await data.get_unique_equip_info(id_, level1, 1),
            await data.get_unique_equip_info(id_, level2 + 1, 2),
        ]
    else:
        tp_bouns_attr = await data.get_unique_equip_bonus(
            id_,
            level1 - GameSetting.tp_limit_level.value,
            GameSetting.tp_limit_level.value,
        )

        other_bouns_attr = await data.get_unique_equip_bonus(
            id_,
            level1 - GameSetting.other_limit_level.value,
            GameSetting.other_limit_level.value,
        )

        if tp_bouns_attr:
            level1 = GameSetting.tp_limit_level.value  # 带有tp属性，仅计算260级的属性
        elif other_bouns_attr:
            level1 = (
                GameSetting.other_limit_level.value
            )  # 带回避相关属性，仅计算300级之前的属性
        equip_list: List[UniqueEquipInfo] = [
            await data.get_unique_equip_info(id_, level1, 1),
            await data.get_unique_equip_info(id_, level2 + 1, 2),
        ]
        if equip_list[0]:
            if tp_bouns_attr:
                equip_list[0].isTpLimitAction = 1
                equip_list[0].add(tp_bouns_attr)
            if other_bouns_attr:
                equip_list[0].isOtherLimitAction = 1
                equip_list[0].add(other_bouns_attr)

            if skill_info.main_skill_1:
                skills["normal"].append(skill_info.main_skill_1)
            if skill_info.main_skill_evolution_1:
                skills["normal"].append(skill_info.main_skill_evolution_1)
            if skill_info.sp_skill_1:
                skills["sp"].append(skill_info.sp_skill_1)
            if skill_info.sp_skill_evolution_1:
                skills["sp"].append(skill_info.sp_skill_evolution_1)
        if equip_list[1]:
            if skill_info.main_skill_2:
                skills["normal"].append(skill_info.main_skill_2)
            if skill_info.main_skill_evolution_2:
                skills["normal"].append(skill_info.main_skill_evolution_2)
            if skill_info.sp_skill_2:
                skills["sp"].append(skill_info.sp_skill_2)
            if skill_info.sp_skill_evolution_2:
                skills["sp"].append(skill_info.sp_skill_evolution_2)
    equip_list = [equip for equip in equip_list if equip]
    if not equip_list:
        return "暂时没有更新该角色的专武数据"

    _, skill_type_dict = get_skill_ids(skill_info)
    skill_data_dict = {
        skill: await data.get_skill_data(
            temp if (temp := await data.get_rf_skill_id(skill)) else skill
        )
        for skill in skills["normal"] + skills["sp"]
    }
    skill_action_dict = {
        skill: await data.get_skill_actions(
            action_ids=(
                [
                    getattr(skill_data_dict[skill], f"action_{i}")
                    for i in range(1, 10 + 1)
                ]
            )
        )
        for skill in skills["normal"] + skills["sp"]
    }
    if type_ == "tw":
        equip_list = [convert2simplified(equip) for equip in equip_list]
        skill_data_dict = {k: convert2simplified(v) for k, v in skill_data_dict.items()}
        skill_action_dict = {
            k: [convert2simplified(q) for q in v] for k, v in skill_action_dict.items()
        }

    img_list = [
        await draw_char_icon(id_, 500),
        await draw_unique_equipment(equip_list, [orginal_level1, orginal_level2]),
        await draw_all_skill(
            skills, skill_type_dict, skill_data_dict, skill_action_dict
        ),
    ]
    return pic2cqcode(merge_pic(img_list))


def group_story(story: List[CharaStoryStatusData]):
    data = DefaultDict(list)
    for item in story:
        if item.title and item.sub_title:
            data[item.story_id // 1000].append(item)
    return data


@fetch_chara_data
async def get_chara_story(id_: int, type_: str = None, data: PCRDatabase = None):

    story_list = await data.get_chara_story_status(id_)
    if type_ == "tw":
        story_list = [convert2simplified(story) for story in story_list]

    story_dict: Dict[int, List[CharaStoryStatusData]] = group_story(story_list)
    return pic2cqcode(await draw_story(story_dict))


@fetch_chara_data
async def get_chara_skill(id_: int, type_: str = None, data: PCRDatabase = None):
    unit_info = await data.get_unit_info_query(id_)
    attack_pattern = await data.get_attack_pattern(
        unit_info.cutin1_star6 or unit_info.unit_id
    )
    unit_skills: UnitSkillData = await data.get_unit_skill(
        unit_info.cutin1_star6 or unit_info.unit_id
    )
    skill_dict, skill_type_dict = get_skill_ids(unit_skills)
    skill_data_dict = {
        skill: await data.get_skill_data(
            temp if (temp := await data.get_rf_skill_id(skill)) else skill
        )
        for skill in skill_dict["normal"] + skill_dict["sp"]
    }
    skill_action_dict = {
        skill: await data.get_skill_actions(
            action_ids=[
                getattr(skill_data_dict[skill], f"action_{i}") for i in range(1, 10 + 1)
            ]
        )
        for skill in skill_dict["normal"] + skill_dict["sp"]
    }
    if type_ == "tw":
        skill_data_dict = {k: convert2simplified(v) for k, v in skill_data_dict.items()}
        skill_action_dict = {
            k: [convert2simplified(q) for q in v] for k, v in skill_action_dict.items()
        }
    return pic2cqcode(
        merge_pic(
            [
                await draw_char_icon(id_, 500),
                await draw_pattern(attack_pattern, unit_skills, skill_data_dict),
                await draw_all_skill(
                    skill_dict, skill_type_dict, skill_data_dict, skill_action_dict
                ),
            ]
        )
    )


@judge_platform
async def get_enemy_id(
    clan_battle_id: int,
    phase: int,
    boss_id: int,
    type_: str = None,
    data: PCRDatabase = None,
):
    clan_info = await data.get_all_clan_battle_data(clan_battle_id)
    unit_ids = clan_info[0].unit_ids.split("-")
    enemy_ids = clan_info[0].enemy_ids.split("-")
    order = boss_id - 1 + 5 * (phase - clan_info[0].min_phase)
    return unit_ids[order], enemy_ids[order]


@judge_platform
async def get_enemy_skill(
    id_: int, type_: str = None, data: PCRDatabase = None, enemy_id: int = None
):
    unit_info = await data.get_enemy_info_query(id_)
    attack_pattern = await data.get_attack_pattern(
        unit_info.cutin_star6 or unit_info.unit_id
    )
    unit_skills: UnitSkillData = await data.get_unit_skill(
        unit_info.cutin_star6 or unit_info.unit_id
    )
    skill_dict, skill_type_dict = get_skill_ids(unit_skills)
    skill_data_dict = {
        skill: await data.get_skill_data(skill)
        for skill in skill_dict["normal"] + skill_dict["sp"]
    }
    skill_action_dict = {
        skill: await data.get_skill_actions(
            action_ids=[
                getattr(skill_data_dict[skill], f"action_{i}") for i in range(1, 10 + 1)
            ]
        )
        for skill in skill_dict["normal"] + skill_dict["sp"]
    }
    if type_ == "tw":
        skill_data_dict = {k: convert2simplified(v) for k, v in skill_data_dict.items()}
        skill_action_dict = {
            k: [convert2simplified(q) for q in v] for k, v in skill_action_dict.items()
        }
    main_parameter = await data.get_enemy_parameter_query(enemy_id)
    skill_level_dict = get_skill_level(unit_skills, main_parameter)

    sub = await data.get_enemy_m_parts_query(enemy_id)
    sub_parameters = (
        [
            await data.get_enemy_parameter_query(part_id)
            for part_id in [
                sub.child_enemy_parameter_1,
                sub.child_enemy_parameter_2,
                sub.child_enemy_parameter_3,
                sub.child_enemy_parameter_4,
                sub.child_enemy_parameter_5,
            ]
            if part_id
        ]
        if sub
        else []
    )
    return pic2cqcode(
        merge_pic(
            [
                await draw_enemy_icon(unit_info.unit_id, unit_info.unit_name, 500),
                await draw_enemy_introduce(main_parameter, sub_parameters),
                await draw_pattern(attack_pattern, unit_skills, skill_data_dict),
                await draw_all_skill(
                    skill_dict,
                    skill_type_dict,
                    skill_data_dict,
                    skill_action_dict,
                    skill_level_dict,
                    (
                        max(
                            *[
                                max(sub_parameter.atk, sub_parameter.magic_str)
                                for sub_parameter in sub_parameters
                            ]
                        )
                        if sub_parameters
                        else max(main_parameter.atk, main_parameter.magic_str)
                    ),
                ),
            ]
        )
    )


@judge_platform
async def get_clan_battle_info(page: int, type_: str = None, data: PCRDatabase = None):
    clan_info = await data.get_all_clan_battle_data(0, page=page)
    count_dict = {
        clan.clan_battle_id: {
            count.multi_enemy_id: count.enemy_part_ids.split("-")
            for count in await data.get_all_clan_battle_target_count(
                clan.clan_battle_id, clan.max_phase
            )
        }
        for clan in clan_info
    }
    return pic2cqcode(await draw_clan_info(clan_info, count_dict))


@judge_platform
async def get_boss_max_time_return_line(
    type_: str = None, data: PCRDatabase = None, clan_battle_id: str = None
):
    if not clan_battle_id:
        clan_info = await data.get_latest_clan_battle_data()
    else:
        clan_info = await data.get_all_clan_battle_data(int(clan_battle_id))
    clan_info = clan_info[0]
    boss_hp_dict = {}
    enemy_ids = clan_info.enemy_ids.split("-")
    for phase in range(clan_info.min_phase, clan_info.max_phase + 1):
        boss_hp_dict[phase] = [
            (await data.get_enemy_parameter_query(enemy_id)).hp
            for enemy_id in enemy_ids[
                5 * (phase - clan_info.min_phase) : 5 * (phase - clan_info.min_phase)
                + 5
            ]
        ]
    damage_dict = {phase: [[] for _ in range(5)] for phase in boss_hp_dict}
    for phase in boss_hp_dict:
        for boss, hp in enumerate(boss_hp_dict[phase]):
            num = 1
            damage = cal_damage_by_max_time_return(hp, num)

            while damage > 600 * 10**4 and num <= 8:
                num += 1
                damage_dict[phase][boss].append(damage)  # 每次增加1个满补线
                damage = cal_damage_by_max_time_return(hp, num)

    phase_lap_dict = {}
    for phase_data in await data.get_phase_lap_form_to(clan_info.clan_battle_id):
        if phase_data.phase not in phase_lap_dict:
            phase_lap_dict[phase_data.phase] = (
                phase_data.lap_num_from,
                phase_data.lap_num_to,
            )
        else:
            phase_lap_dict[phase_data.phase] = (
                min(phase_lap_dict[phase_data.phase][0], phase_data.lap_num_from),
                max(phase_lap_dict[phase_data.phase][1], phase_data.lap_num_to),
            )

    return pic2cqcode(
        draw_max_boss_time_return(
            damage_dict,
            boss_hp_dict,
            phase_lap_dict,
            clan_info.clan_battle_id,
            clan_info.start_time[:10],
        )
    )


def fliter_event_list(
    event_list: List[
        Union[
            EventData,
            CampaignFreegachaData,
            BirthdayData,
            GachaHistoryData,
            CalendarEvent,
            ClanBattleData,
        ]
    ],
    is_fix_jp=False,
):
    in_progress_list = []
    coming_soon_list = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for event in event_list:
        if is_in_progress(now, event.start_time, event.end_time, is_fix_jp):
            in_progress_list.append(event)
        elif is_coming_soon(now, event.start_time, is_fix_jp):
            coming_soon_list.append(event)
    in_progress_list.sort(key=lambda x: x.start_time)
    coming_soon_list.sort(key=lambda x: x.start_time)
    return in_progress_list, coming_soon_list


@judge_platform
async def get_schedule(type_: str = None, data: PCRDatabase = None):
    # fes_uid = await data.get_fes_unit_id_list()

    calendar_event_list = (
        await data.get_all_events()
        + await data.get_free_gacha_event()
        + await data.get_gacha_history()
        + await data.get_drop_event()
        + await data.get_mission_event()
        + await data.get_login_event()
        + await data.get_fortune_event()
        + await data.get_tower_event()
        + await data.get_sp_dungeon_event()
        + await data.get_fault_event()
        + await data.get_all_clan_battle_data()
    )
    try:
        calendar_event_list += await data.get_colosseum_event()
    except Exception as e:
        logger.warning(f"获取斗技场事件失败: {e}")

    is_fix_jp = type_ == "jp"
    in_progress_list, coming_soon_list = fliter_event_list(
        calendar_event_list, is_fix_jp
    )
    now = datetime.now()
    birthday_list = await data.get_birthday_list(now.timestamp(), 7)
    for birthday in birthday_list:
        if birthday.day == now.day and birthday.month == now.month:
            in_progress_list.append(birthday)
        else:
            coming_soon_list.append(birthday)

    img_list = []
    split_index = len(in_progress_list)
    for event in in_progress_list + coming_soon_list:
        if isinstance(event, EventData):
            img_list.append(await draw_story_event(event, type_))
        elif isinstance(event, CampaignFreegachaData):
            img_list.append(await draw_free_gacha_event(event))
        elif isinstance(event, BirthdayData):
            img_list.append(await draw_birthday(event))
        elif isinstance(event, ClanBattleData):
            img_list.append(await draw_clan_battle_event(event))
        elif isinstance(event, CalendarEvent):
            img_list.append(await drwa_calendar_event(event))
        elif isinstance(event, GachaHistoryData):
            unit_dict = {
                unit_id: (await data.get_unit_info_query(int(unit_id)))
                for unit_id in event.unit_ids.split("-")
            }
            img_list.append(await draw_gacha_event(event, unit_dict))
        else:
            print(f"未知事件类型: {type(event)}")
    return pic2cqcode(
        merge_pic(
            [
                merge_pic(img_list[:split_index]),
                merge_pic(img_list[split_index:]),
            ],
            direction="horizontal",
        )
    )
