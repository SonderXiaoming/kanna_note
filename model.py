from dataclasses import dataclass
from typing import List, Optional

from .base import CalendarEventType, Color


@dataclass
class UnitInfo:
    unit_id: int = 0
    unit_name: str = ""
    kana: str = ""
    rarity: int = 0
    age_int: int = 0
    guild: Optional[str] = None
    race: Optional[str] = None
    voice: Optional[str] = None
    blood_type: Optional[str] = None
    favorite: Optional[str] = None
    catch_copy: Optional[str] = None
    self_text: Optional[str] = None
    height_int: Optional[int] = None
    weight_int: Optional[int] = None
    birth_month_int: Optional[int] = None
    birth_day_int: Optional[int] = None
    search_area_width: Optional[int] = None
    atk_type: Optional[int] = None
    intro: str = ""
    unit_start_time: str = ""
    actual_name: str = ""
    cutin1_star6: int = 0  # 6星卡通常为自身，小概率变成奇怪的东西 比如六星吉他
    limit_type: Optional[int] = None


@dataclass
class UniqueEquipBonus:
    hp: float = 0
    atk: float = 0
    magic_str: float = 0
    def_: float = 0  # 避免与 Python 关键字 `def` 冲突
    magic_def: float = 0
    physical_critical: float = 0
    magic_critical: float = 0
    wave_hp_recovery: float = 0
    wave_energy_recovery: float = 0
    dodge: float = 0
    physical_penetrate: float = 0
    magic_penetrate: float = 0
    life_steal: float = 0
    hp_recovery_rate: float = 0
    energy_recovery_rate: float = 0
    energy_reduce_rate: float = 0
    accuracy: float = 0


@dataclass
class UniqueEquipInfo:
    unit_id: int = 0
    equipment_id: int = 0
    equipment_name: str = ""
    description: str = ""
    hp: float = 0
    atk: float = 0
    magic_str: float = 0
    def_: float = 0
    magic_def: float = 0
    physical_critical: float = 0
    magic_critical: float = 0
    wave_hp_recovery: float = 0
    wave_energy_recovery: float = 0
    dodge: float = 0
    physical_penetrate: float = 0
    magic_penetrate: float = 0
    life_steal: float = 0
    hp_recovery_rate: float = 0
    energy_recovery_rate: float = 0
    energy_reduce_rate: float = 0
    accuracy: Optional[float] = None  # 可能为 NULL
    isTpLimitAction: int = 0  # 固定值 0
    isOtherLimitAction: int = 0  # 固定值 0

    def add(self, other: UniqueEquipBonus):
        self.hp += other.hp
        self.atk += other.atk
        self.magic_str += other.magic_str
        self.def_ += other.def_
        self.magic_def += other.magic_def
        self.physical_critical += other.physical_critical
        self.magic_critical += other.magic_critical
        self.wave_hp_recovery += other.wave_hp_recovery
        self.wave_energy_recovery += other.wave_energy_recovery
        self.dodge += other.dodge
        self.physical_penetrate += other.physical_penetrate
        self.magic_penetrate += other.magic_penetrate
        self.life_steal += other.life_steal
        self.hp_recovery_rate += other.hp_recovery_rate
        self.energy_recovery_rate += other.energy_recovery_rate
        self.energy_reduce_rate += other.energy_reduce_rate
        self.accuracy += other.accuracy


@dataclass
class CharaStoryStatusData:
    story_id: int
    title: str
    sub_title: str
    status_type_1: Optional[int]
    status_rate_1: Optional[int]
    status_type_2: Optional[int]
    status_rate_2: Optional[int]
    status_type_3: Optional[int]
    status_rate_3: Optional[int]
    status_type_4: Optional[int]
    status_rate_4: Optional[int]
    status_type_5: Optional[int]
    status_rate_5: Optional[int]


@dataclass
class SkillActionData:
    action_id: int
    class_id: int
    action_type: int
    action_detail_1: int
    action_detail_2: int
    action_detail_3: int
    action_value_1: float
    action_value_2: float
    action_value_3: float
    action_value_4: float
    action_value_5: float
    action_value_6: float
    action_value_7: float
    target_assignment: int
    target_area: int
    target_range: int
    target_type: int
    target_number: int
    target_count: int
    discription: str
    level_up_disp: str
    ailment_name: str
    isRfSkill: int
    isOtherRfSkill: int


@dataclass
class SkillActionText:
    actionId: int
    tag: str
    action_desc: str
    summon_unit_id: int
    show_coe: bool


@dataclass
class ShowCoe:
    action_index: int
    coe_type: int
    coe: str


@dataclass
class ClanBattleData:
    clan_battle_id: int
    release_month: Optional[int]
    start_time: Optional[str]
    min_phase: Optional[int]
    max_phase: Optional[int]
    enemy_ids: Optional[str]
    unit_ids: Optional[str]
    end_time: Optional[str] = None


@dataclass
class ClanBattleTargetData:
    clan_battle_id: int
    multi_enemy_id: Optional[int]
    enemy_part_ids: Optional[str]


@dataclass
class CampaignFreegachaData:
    id: int
    max_count: int
    start_time: str
    end_time: str


@dataclass
class EventData:
    event_id: int
    story_id: int
    original_event_id: int
    start_time: str
    end_time: str
    title: str
    unit_ids: Optional[str]


@dataclass
class CalendarEventData:
    title: str
    multiple: str
    info: str
    color: str = Color.primary.value


@dataclass
class CalendarEvent:
    type: str = ""
    value: int = 0
    start_time: str = ""
    end_time: str = ""

    def get_event_list(self) -> List[CalendarEventData]:
        events = []
        try:
            type_int = int(self.type)
        except Exception:
            type_int = 404
        event_type = CalendarEventType.get_by_value(type_int)

        if event_type == CalendarEventType.TOWER:
            events.append(CalendarEventData("露娜塔", "", ""))
        elif event_type == CalendarEventType.SP_DUNGEON:
            events.append(CalendarEventData("特殊地下城", "", ""))
        elif event_type == CalendarEventType.TDF:
            events.append(CalendarEventData("次元断层", "", ""))
        elif event_type == CalendarEventType.COLOSSEUM:
            events.append(CalendarEventData("斗技场", "", ""))
        else:
            try:
                list_of_types = list(map(int, self.type.split("-")))
            except Exception:
                list_of_types = [self.type]
            for type_val in list_of_types:
                event_enum = CalendarEventType.get_by_value(type_val)

                title_map = {
                    CalendarEventType.DAILY: "每日任务体力",
                    CalendarEventType.LOGIN: "每日登录宝石奖励，共计",
                    CalendarEventType.FORTUNE: "兰德索尔杯",
                    CalendarEventType.N_DROP: "普通关卡",
                    CalendarEventType.N_MANA: "普通关卡",
                    CalendarEventType.H_DROP: "困难关卡",
                    CalendarEventType.H_MANA: "困难关卡",
                    CalendarEventType.VH_DROP: "高难关卡",
                    CalendarEventType.VH_MANA: "高难关卡",
                    CalendarEventType.EXPLORE: "探索",
                    CalendarEventType.SHRINE: "圣迹调查",
                    CalendarEventType.TEMPLE: "神殿调查",
                    CalendarEventType.DUNGEON: "地下城",
                }

                title = title_map.get(event_enum, "")

                multiple = self.value / 1000.0
                if multiple in [1.5, 2.0]:
                    drop_color = Color.gold.value
                elif multiple in [2.5, 3.0]:
                    drop_color = Color.red.value
                elif multiple == 4.0:
                    drop_color = Color.green.value
                elif multiple == 5.0:
                    drop_color = Color.orange.value
                else:
                    drop_color = Color.primary.value

                if event_enum == CalendarEventType.LOGIN:
                    mult_text = str(self.value)
                elif event_enum == CalendarEventType.FORTUNE:
                    mult_text = ""
                else:
                    mult_text = (
                        f"x{int(multiple)}倍"
                        if int(multiple * 10) % 10 == 0
                        else f"x{multiple}倍"
                    )

                info = ""
                if event_enum not in [
                    CalendarEventType.DAILY,
                    CalendarEventType.LOGIN,
                    CalendarEventType.FORTUNE,
                ]:
                    info = "玛那掉落量" if type_val > 40 else "掉落量"

                events.append(CalendarEventData(title, mult_text, info, drop_color))

        return events


@dataclass
class BirthdayData:
    month: int = 0
    day: int = 0
    unit_ids: str = ""
    unit_names: str = ""


@dataclass
class GachaHistoryData:
    gacha_id: int
    gacha_name: str
    ids: Optional[str]
    unit_ids: Optional[str]
    unit_names: Optional[str]
    is_limiteds: Optional[str]
    is_ups: Optional[str]
    description: Optional[str]
    start_time: Optional[str]
    end_time: Optional[str]
