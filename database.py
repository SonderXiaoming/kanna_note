import asyncio
import contextlib
import datetime
import sqlite3
from functools import wraps
from pathlib import Path
from typing import (
    Any,
    Awaitable,
    Callable,
    Concatenate,
    List,
    Optional,
    ParamSpec,
    Tuple,
    TypeVar,
    Union,
    overload,
)

from loguru import logger
from sqlalchemy import (
    Integer,
    alias,
    case,
    cast,
    func,
    literal,
    or_,
    text,
    tuple_,
    union_all,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.sql.functions import coalesce
from sqlmodel import select

from .base import FilePath
from .model import (
    BirthdayData,
    CalendarEvent,
    CampaignFreegachaData,
    CharaStoryStatusData,
    ClanBattleData,
    ClanBattleTargetData,
    EventData,
    GachaHistoryData,
    SkillActionData,
    UniqueEquipBonus,
    UniqueEquipInfo,
    UnitInfo,
)
from .table import (
    AbyssEnemyParameter,
    AbyssSchedule,
    AcnEnemyParameter,
    ActualUnitBackground,
    AilmentData,
    CampaignFreegacha,
    CampaignSchedule,
    CharaFortuneSchedule,
    CharaIdentity,
    CharaStoryStatus,
    ClanBattle2MapData,
    ClanBattleSchedule,
    ColosseumScheduleData,
    DailyMissionData,
    DomeScheduleData,
    EnemyMParts,
    EnemyParameter,
    EnemyTalentWeakness,
    EventEnemyParameter,
    EventStoryData,
    EventStoryDetail,
    ExUniqueEquipment1,
    GachaData,
    GachaExchangeLineup,
    HatsuneSchedule,
    HuntEnemyParameter,
    InvasionEnemyParameter,
    LabyrinthEnemyParameter,
    LoginBonusData,
    LoginBonusDetail,
    MirageEnemyParameter,
    MissionRewardData,
    MreEnemyParameter,
    RedeemUnit,
    SecretDungeonSchedule,
    SekaiEnemyParameter,
    SevenEnemyParameter,
    SevenEventSetting,
    SevenSchedule,
    ShioriEnemyParameter,
    ShioriEventList,
    SkillAction,
    SkillData,
    SpSkillLabelData,
    SreEnemyParameter,
    StoryDetail,
    TalentQuestEnemyParameter,
    TalentWeakness,
    TdfSchedule,
    TowerEnemyParameter,
    TowerSchedule,
    UniqueEquipEnhanceRate,
    UniqueEquipmentData,
    UniqueEquipmentEnhanceData,
    UnitAttackPattern,
    UnitData,
    UnitEnemyData,
    UnitProfile,
    UnitRoleData,
    UnitSkillData,
    UnitSkillDataRF,
    UnitTalent,
    UnitUniqueEquipment,
    WaveGroupData,
)

T = TypeVar("T")
P = ParamSpec("P")


@overload
def session(
    func: Callable[Concatenate[Any, "AsyncSession", P], Awaitable[T]],
) -> Callable[Concatenate[Any, P], Awaitable[T]]: ...


def session(
    func: Callable[Concatenate[Any, AsyncSession, P], Awaitable[T]],
) -> Callable[Concatenate[Any, P], Awaitable[T]]:
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        async with self.async_session() as _session, _session.begin():
            return await func(self, _session, *args, **kwargs)

    return wrapper  # 返回包装后的函数


def convert_invalid_values(column):
    return cast(
        case(
            (
                or_(
                    column.like("%-%"),
                    column.like("%?%"),
                    column.like("%？%"),
                    column == 0,
                ),
                -1,
            ),
            else_=column,
        ),
        Integer,
    )


KANNA_IDS = [170101, 170201]

ENEMY_PARAMETER_QUERY_SPECS = (
    (EnemyParameter, EnemyParameter.enemy_id),
    (TalentQuestEnemyParameter, TalentQuestEnemyParameter.enemy_id),
    (SevenEnemyParameter, SevenEnemyParameter.enemy_id),
    (EventEnemyParameter, EventEnemyParameter.enemy_id),
    (ShioriEnemyParameter, ShioriEnemyParameter.enemy_id),
    (SreEnemyParameter, SreEnemyParameter.enemy_id),
    (TowerEnemyParameter, TowerEnemyParameter.enemy_id),
    (AbyssEnemyParameter, AbyssEnemyParameter.enemy_id),
    (AcnEnemyParameter, AcnEnemyParameter.enemy_id),
    (HuntEnemyParameter, HuntEnemyParameter.enemy_id),
    (InvasionEnemyParameter, InvasionEnemyParameter.enemy_id),
    (LabyrinthEnemyParameter, LabyrinthEnemyParameter.enemy_id),
    (MirageEnemyParameter, MirageEnemyParameter.enemy_id),
    (MreEnemyParameter, MreEnemyParameter.enemy_id),
    (SekaiEnemyParameter, SekaiEnemyParameter.sekai_enemy_id),
)


class PCRDatabase:
    def __init__(self, url: str):
        self.db_path = url
        self.url = f"sqlite+aiosqlite:///{url}"
        self.engine = create_async_engine(self.url, pool_recycle=1500)
        self.async_session = async_sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )
        self.all_chaeacters = []
        self.ex_character = []
        self.max_unique_equip_lv = [1, 1]

    async def init(self):
        # 三服数据库都原生提供下列扩展技能字段后，删除此调用和对应方法。
        await self.ensure_skill_columns()
        self.all_chaeacters = await self.get_all_units_list()
        self.ex_character = await self.get_ex_units_list()
        self.max_unique_equip_lv[0] = await self.get_max_unique_equip_lv(1)
        self.max_unique_equip_lv[1] = await self.get_max_unique_equip_lv(2)

    @session
    async def ensure_skill_columns(self, session: AsyncSession):
        """补齐各区服尚未上线的新版正式技能字段。"""
        result = await session.execute(text("PRAGMA table_info(unit_skill_data)"))
        unit_skill_columns = {row[1] for row in result.fetchall()}
        for column in (
            "main_skill_revolution_1",
            "main_skill_revolution_2",
            "sp_skill_revolution_1",
            "sp_skill_revolution_2",
        ):
            if column not in unit_skill_columns:
                await session.execute(
                    text(
                        f"ALTER TABLE unit_skill_data ADD COLUMN {column} "
                        "INTEGER NOT NULL DEFAULT 0"
                    )
                )

        result = await session.execute(text("PRAGMA table_info(skill_data)"))
        skill_columns = {row[1] for row in result.fetchall()}
        for num in range(11, 21):
            for prefix in ("action", "depend_action"):
                column = f"{prefix}_{num}"
                if column not in skill_columns:
                    await session.execute(
                        text(
                            f"ALTER TABLE skill_data ADD COLUMN {column} "
                            "INTEGER NOT NULL DEFAULT 0"
                        )
                    )

    @session
    async def get_ex_units_list(self, session: AsyncSession) -> list[int]:
        result = await session.execute(select(RedeemUnit.unit_id).distinct())
        return result.scalars().all()

    @session
    async def get_all_units_list(self, session: AsyncSession) -> list[int]:
        result = await session.execute(select(UnitData.unit_id).distinct())
        return result.scalars().all()

    @session
    async def get_max_unique_equip_lv(self, session: AsyncSession, solt: int) -> int:
        result = await session.execute(
            select(func.max(UniqueEquipmentEnhanceData.enhance_level)).where(
                UniqueEquipmentEnhanceData.equip_slot == solt
            )
        )
        return result.scalars().first() or 1

    @session
    async def get_unit_info_query(
        self, session: AsyncSession, unit_id: int
    ) -> UnitInfo:
        # 处理 `limit_type` 的 CASE 语句
        limit_type_case = case(
            (UnitData.is_limited == 0, 1),
            ((UnitData.is_limited == 1) & (UnitData.rarity == 3), 2),
            ((UnitData.is_limited == 1) & (UnitData.rarity == 1), 3),
            (UnitData.is_limited == 1, 4),
            else_=None,
        ).label("limit_type")

        # 处理异常数据转换（年龄、身高、体重、生日）

        age_int = convert_invalid_values(UnitProfile.age).label("age_int")
        height_int = convert_invalid_values(UnitProfile.height).label("height_int")
        weight_int = convert_invalid_values(UnitProfile.weight).label("weight_int")
        birth_month_int = convert_invalid_values(UnitProfile.birth_month).label(
            "birth_month_int"
        )
        birth_day_int = convert_invalid_values(UnitProfile.birth_day).label(
            "birth_day_int"
        )

        # 构建查询
        query = (
            select(
                UnitData.unit_id,
                UnitData.unit_name,
                coalesce(UnitData.kana, "").label("kana"),
                UnitData.rarity,
                age_int,
                UnitProfile.guild,
                UnitProfile.race,
                UnitProfile.voice,
                UnitProfile.blood_type,
                UnitProfile.favorite,
                UnitProfile.catch_copy,
                UnitProfile.self_text,
                height_int,
                weight_int,
                birth_month_int,
                birth_day_int,
                UnitData.search_area_width,
                UnitData.atk_type,
                UnitData.normal_atk_cast_time,
                coalesce(UnitTalent.talent_id, 0).label("talent_id"),
                coalesce(UnitRoleData.unit_role_id, 0).label("unit_role_id"),
                coalesce(UnitData.comment, "......").label("intro"),
                coalesce(UnitData.start_time, text("'2015/04/01'")).label(
                    "unit_start_time"
                ),
                coalesce(ActualUnitBackground.unit_name, "").label("actual_name"),
                UnitData.cutin1_star6,
                limit_type_case,
            )
            .select_from(UnitData)
            .join(UnitProfile, UnitProfile.unit_id == UnitData.unit_id, isouter=True)
            .join(
                ActualUnitBackground,
                ((UnitData.unit_id // 100) == (ActualUnitBackground.unit_id // 100)),
                isouter=True,
            )
            .join(UnitTalent, UnitTalent.unit_id == UnitData.unit_id, isouter=True)
            .join(UnitRoleData, UnitRoleData.unit_id == UnitData.unit_id, isouter=True)
            .where(UnitData.unit_id == unit_id)
        )
        result = await session.execute(query)
        row = result.first()
        if row is None:
            logger.warning(f"unit_data does not contain unit_id={unit_id}")
            return UnitInfo(unit_id=unit_id)
        unit_info = UnitInfo(**dict(zip(UnitInfo.__annotations__.keys(), row)))
        if unit_info.unit_id in KANNA_IDS:
            unit_info.limit_type = 2
        elif unit_info.unit_id in self.ex_character:
            unit_info.limit_type = 4
        return unit_info

    @session
    async def get_enemy_info_query(
        self, session: AsyncSession, enemy_id: int
    ) -> UnitEnemyData:
        result = await session.execute(
            select(UnitEnemyData).where(UnitEnemyData.unit_id == enemy_id)
        )
        return result.scalars().first()

    @session
    async def get_enemy_weakness_query(
        self, session: AsyncSession, enemy_id: int
    ) -> Optional[TalentWeakness]:
        result = await session.execute(
            select(TalentWeakness)
            .join(
                EnemyTalentWeakness,
                TalentWeakness.resist_id == EnemyTalentWeakness.resist_id,
            )
            .where(EnemyTalentWeakness.enemy_id == enemy_id)
        )
        return result.scalars().first()

    @session
    async def get_enemy_parameter_query(
        self, session: AsyncSession, enemy_id: int
    ) -> EnemyParameter:
        result = await session.execute(
            select(EnemyParameter).where(EnemyParameter.enemy_id == enemy_id)
        )
        return result.scalars().first()

    @session
    async def get_talent_quest_enemy_parameter_query(
        self, session: AsyncSession, enemy_id: int
    ) -> TalentQuestEnemyParameter:
        result = await session.execute(
            select(TalentQuestEnemyParameter).where(
                TalentQuestEnemyParameter.enemy_id == enemy_id
            )
        )
        return result.scalars().first()

    @session
    async def get_seven_enemy_parameter_query(
        self, session: AsyncSession, enemy_id: int
    ) -> SevenEnemyParameter:
        result = await session.execute(
            select(SevenEnemyParameter).where(SevenEnemyParameter.enemy_id == enemy_id)
        )
        return result.scalars().first()

    @session
    async def get_event_enemy_parameter_query(
        self, session: AsyncSession, enemy_id: int
    ) -> EventEnemyParameter:
        result = await session.execute(
            select(EventEnemyParameter).where(EventEnemyParameter.enemy_id == enemy_id)
        )
        return result.scalars().first()

    @session
    async def get_shiori_enemy_parameter_query(
        self, session: AsyncSession, enemy_id: int
    ) -> ShioriEnemyParameter:
        result = await session.execute(
            select(ShioriEnemyParameter).where(
                ShioriEnemyParameter.enemy_id == enemy_id
            )
        )
        return result.scalars().first()

    @session
    async def get_sre_enemy_parameter_query(
        self, session: AsyncSession, enemy_id: int
    ) -> SreEnemyParameter:
        result = await session.execute(
            select(SreEnemyParameter).where(SreEnemyParameter.enemy_id == enemy_id)
        )
        return result.scalars().first()

    @session
    async def get_tower_enemy_parameter_query(
        self, session: AsyncSession, enemy_id: int
    ) -> TowerEnemyParameter:
        result = await session.execute(
            select(TowerEnemyParameter).where(TowerEnemyParameter.enemy_id == enemy_id)
        )
        return result.scalars().first()

    @session
    async def resolve_enemy_parameter(self, session: AsyncSession, enemy_id: int):
        for model, id_column in ENEMY_PARAMETER_QUERY_SPECS:
            with contextlib.suppress(Exception):
                result = await session.execute(
                    select(model).where(id_column == enemy_id)
                )
                if parameter := result.scalars().first():
                    return parameter
        return None

    @session
    async def get_enemy_m_parts_query(
        self, session: AsyncSession, enemy_id: int
    ) -> EnemyMParts:
        result = await session.execute(
            select(EnemyMParts).where(EnemyMParts.enemy_id == enemy_id)
        )
        return result.scalars().first()

    @session
    async def get_unique_equip_bonus(
        self, session: AsyncSession, unit_id: int, lv: int, min_lv: int
    ):

        # 构建查询
        query = (
            select(
                (UniqueEquipEnhanceRate.hp * coalesce(lv, 0)).label("hp"),
                (UniqueEquipEnhanceRate.atk * coalesce(lv, 0)).label("atk"),
                (UniqueEquipEnhanceRate.magic_str * coalesce(lv, 0)).label("magic_str"),
                (UniqueEquipEnhanceRate.def_ * coalesce(lv, 0)).label("def"),
                (UniqueEquipEnhanceRate.magic_def * coalesce(lv, 0)).label("magic_def"),
                (UniqueEquipEnhanceRate.physical_critical * coalesce(lv, 0)).label(
                    "physical_critical"
                ),
                (UniqueEquipEnhanceRate.magic_critical * coalesce(lv, 0)).label(
                    "magic_critical"
                ),
                (UniqueEquipEnhanceRate.wave_hp_recovery * coalesce(lv, 0)).label(
                    "wave_hp_recovery"
                ),
                (UniqueEquipEnhanceRate.wave_energy_recovery * coalesce(lv, 0)).label(
                    "wave_energy_recovery"
                ),
                (UniqueEquipEnhanceRate.dodge * coalesce(lv, 0)).label("dodge"),
                (UniqueEquipEnhanceRate.physical_penetrate * coalesce(lv, 0)).label(
                    "physical_penetrate"
                ),
                (UniqueEquipEnhanceRate.magic_penetrate * coalesce(lv, 0)).label(
                    "magic_penetrate"
                ),
                (UniqueEquipEnhanceRate.life_steal * coalesce(lv, 0)).label(
                    "life_steal"
                ),
                (UniqueEquipEnhanceRate.hp_recovery_rate * coalesce(lv, 0)).label(
                    "hp_recovery_rate"
                ),
                (UniqueEquipEnhanceRate.energy_recovery_rate * coalesce(lv, 0)).label(
                    "energy_recovery_rate"
                ),
                (UniqueEquipEnhanceRate.energy_reduce_rate * coalesce(lv, 0)).label(
                    "energy_reduce_rate"
                ),
                (UniqueEquipEnhanceRate.accuracy * coalesce(lv, 0)).label("accuracy"),
            )
            .join(
                UnitUniqueEquipment,
                UnitUniqueEquipment.equip_id == UniqueEquipEnhanceRate.equipment_id,
                isouter=True,
            )
            .where(
                UnitUniqueEquipment.unit_id == unit_id,
                UniqueEquipEnhanceRate.min_lv == min_lv + 1,
            )
        )

        # 执行查询
        result = await session.execute(query)
        if result := result.first():
            return UniqueEquipBonus(
                **dict(zip(UniqueEquipBonus.__annotations__.keys(), result))
            )

        else:
            return None

    @session
    async def get_unique_equip_info(
        self, session: AsyncSession, unit_id: int, lv: int = 1, slot: int = 1
    ):

        # 计算属性值
        lv_minus_1 = coalesce(lv - 1, 0)  # 确保 :lv 为空时不会报错

        query = (
            select(
                UnitUniqueEquipment.unit_id,
                UniqueEquipmentData.equipment_id,
                UniqueEquipmentData.equipment_name,
                UniqueEquipmentData.description,
                (UniqueEquipmentData.hp + UniqueEquipEnhanceRate.hp * lv_minus_1).label(
                    "hp"
                ),
                (
                    UniqueEquipmentData.atk + UniqueEquipEnhanceRate.atk * lv_minus_1
                ).label("atk"),
                (
                    UniqueEquipmentData.magic_str
                    + UniqueEquipEnhanceRate.magic_str * lv_minus_1
                ).label("magic_str"),
                (
                    UniqueEquipmentData.def_ + UniqueEquipEnhanceRate.def_ * lv_minus_1
                ).label("def"),
                (
                    UniqueEquipmentData.magic_def
                    + UniqueEquipEnhanceRate.magic_def * lv_minus_1
                ).label("magic_def"),
                (
                    UniqueEquipmentData.physical_critical
                    + UniqueEquipEnhanceRate.physical_critical * lv_minus_1
                ).label("physical_critical"),
                (
                    UniqueEquipmentData.magic_critical
                    + UniqueEquipEnhanceRate.magic_critical * lv_minus_1
                ).label("magic_critical"),
                (
                    UniqueEquipmentData.wave_hp_recovery
                    + UniqueEquipEnhanceRate.wave_hp_recovery * lv_minus_1
                ).label("wave_hp_recovery"),
                (
                    UniqueEquipmentData.wave_energy_recovery
                    + UniqueEquipEnhanceRate.wave_energy_recovery * lv_minus_1
                ).label("wave_energy_recovery"),
                (
                    UniqueEquipmentData.dodge
                    + UniqueEquipEnhanceRate.dodge * lv_minus_1
                ).label("dodge"),
                (
                    UniqueEquipmentData.physical_penetrate
                    + UniqueEquipEnhanceRate.physical_penetrate * lv_minus_1
                ).label("physical_penetrate"),
                (
                    UniqueEquipmentData.magic_penetrate
                    + UniqueEquipEnhanceRate.magic_penetrate * lv_minus_1
                ).label("magic_penetrate"),
                (
                    UniqueEquipmentData.life_steal
                    + UniqueEquipEnhanceRate.life_steal * lv_minus_1
                ).label("life_steal"),
                (
                    UniqueEquipmentData.hp_recovery_rate
                    + UniqueEquipEnhanceRate.hp_recovery_rate * lv_minus_1
                ).label("hp_recovery_rate"),
                (
                    UniqueEquipmentData.energy_recovery_rate
                    + UniqueEquipEnhanceRate.energy_recovery_rate * lv_minus_1
                ).label("energy_recovery_rate"),
                (
                    UniqueEquipmentData.energy_reduce_rate
                    + UniqueEquipEnhanceRate.energy_reduce_rate * lv_minus_1
                ).label("energy_reduce_rate"),
                (
                    UniqueEquipmentData.accuracy
                    + UniqueEquipEnhanceRate.accuracy * lv_minus_1
                ).label("accuracy"),
                literal(0).label("isTpLimitAction"),  # 固定值
                literal(0).label("isOtherLimitAction"),  # 固定值
            )
            .join(
                UniqueEquipmentData,
                UnitUniqueEquipment.equip_id == UniqueEquipmentData.equipment_id,
                isouter=True,
            )
            .join(
                UniqueEquipEnhanceRate,
                UniqueEquipmentData.equipment_id == UniqueEquipEnhanceRate.equipment_id,
                isouter=True,
            )
            .where(
                UniqueEquipmentData.equipment_id is not None,  # 确保装备存在
                UnitUniqueEquipment.unit_id == unit_id,
                UniqueEquipEnhanceRate.min_lv <= 2,
                UniqueEquipmentData.equipment_id % 10 == slot,  # 处理 slot 过滤
            )
        )
        result = await session.execute(query)
        if result := result.first():
            return UniqueEquipInfo(
                **dict(zip(UniqueEquipInfo.__annotations__.keys(), result))
            )

        else:
            return None

    @session
    async def get_unique_equip_1sp_info(
        self, session: AsyncSession, unit_id: int
    ) -> Optional[UniqueEquipInfo]:
        """
        获取专武1sp信息

        Args:
            unit_id: 角色编号

        Returns:
            UniqueEquipInfo对象，如果不存在则返回None
        """
        query = (
            select(
                UnitData.unit_id,
                UniqueEquipmentData.equipment_id,
                UniqueEquipmentData.equipment_name,
                UniqueEquipmentData.description,
                ExUniqueEquipment1.hp,
                ExUniqueEquipment1.attack.label("atk"),
                ExUniqueEquipment1.magic_attack.label("magic_str"),
                ExUniqueEquipment1.defense.label("def"),
                ExUniqueEquipment1.magic_defense.label("magic_def"),
                ExUniqueEquipment1.critical.label("physical_critical"),
                ExUniqueEquipment1.magic_critical,
                ExUniqueEquipment1.wave_hp_recovery,
                ExUniqueEquipment1.wave_energy_recovery,
                ExUniqueEquipment1.dodge,
                ExUniqueEquipment1.penetration.label("physical_penetrate"),
                ExUniqueEquipment1.magic_penetration.label("magic_penetrate"),
                ExUniqueEquipment1.life_steal,
                ExUniqueEquipment1.hp_recovery_rate,
                ExUniqueEquipment1.energy_recovery_rate,
                ExUniqueEquipment1.energy_reduce_rate,
                ExUniqueEquipment1.accuracy,
                literal(0).label("isTpLimitAction"),
            )
            .join(
                UnitUniqueEquipment,
                UnitUniqueEquipment.equip_id == ExUniqueEquipment1.equipment_id,
                isouter=True,
            )
            .join(
                UniqueEquipmentData,
                UniqueEquipmentData.equipment_id == ExUniqueEquipment1.equipment_id,
                isouter=True,
            )
            .join(
                UnitData,
                UnitData.unit_id == UnitUniqueEquipment.unit_id,
                isouter=True,
            )
            .where(
                ExUniqueEquipment1.equipment_id.isnot(None),
                UnitData.unit_id == unit_id,
            )
        )

        result = await session.execute(query)
        if result := result.first():
            return UniqueEquipInfo(
                **dict(zip(UniqueEquipInfo.__annotations__.keys(), result))
            )
        return None

    @session
    async def get_chara_story_status(self, session: AsyncSession, unit_id: int):

        # 构建查询
        query = (
            select(
                CharaStoryStatus.story_id,
                coalesce(StoryDetail.title, "").label("title"),
                coalesce(StoryDetail.sub_title, "").label("sub_title"),
                CharaStoryStatus.status_type_1,
                CharaStoryStatus.status_rate_1,
                CharaStoryStatus.status_type_2,
                CharaStoryStatus.status_rate_2,
                CharaStoryStatus.status_type_3,
                CharaStoryStatus.status_rate_3,
                CharaStoryStatus.status_type_4,
                CharaStoryStatus.status_rate_4,
                CharaStoryStatus.status_type_5,
                CharaStoryStatus.status_rate_5,
            )
            .join(
                CharaIdentity,
                (CharaIdentity.unit_id // 100).in_(
                    [
                        CharaStoryStatus.chara_id_1,
                        CharaStoryStatus.chara_id_2,
                        CharaStoryStatus.chara_id_3,
                        CharaStoryStatus.chara_id_4,
                        CharaStoryStatus.chara_id_5,
                        CharaStoryStatus.chara_id_6,
                        CharaStoryStatus.chara_id_7,
                        CharaStoryStatus.chara_id_8,
                        CharaStoryStatus.chara_id_9,
                        CharaStoryStatus.chara_id_10,
                        CharaStoryStatus.chara_id_11,
                        CharaStoryStatus.chara_id_12,
                        CharaStoryStatus.chara_id_13,
                        CharaStoryStatus.chara_id_14,
                        CharaStoryStatus.chara_id_15,
                        CharaStoryStatus.chara_id_16,
                        CharaStoryStatus.chara_id_17,
                        CharaStoryStatus.chara_id_18,
                        CharaStoryStatus.chara_id_19,
                        CharaStoryStatus.chara_id_20,
                    ]
                ),
                isouter=True,
            )
            .join(
                StoryDetail,
                CharaStoryStatus.story_id == StoryDetail.story_id,
                isouter=True,
            )
            .where(CharaIdentity.unit_id == unit_id)
        )

        # 执行查询
        result = await session.execute(query)

        if result := result.fetchall():
            return [
                CharaStoryStatusData(
                    **dict(zip(CharaStoryStatusData.__annotations__.keys(), item))
                )
                for item in result
            ]
        else:
            return []

    @session
    async def get_unit_skill(
        self, session: AsyncSession, unit_id: int
    ) -> Optional[UnitSkillData]:
        result = await session.execute(
            select(UnitSkillData).where(UnitSkillData.unit_id == unit_id)
        )
        return result.scalar_one_or_none()

    @session
    async def get_skill_data(self, session: AsyncSession, skill_id: int):
        result = await session.execute(
            select(SkillData).where(SkillData.skill_id == skill_id)
        )
        return result.scalar_one_or_none()

    @session
    async def get_skill_actions(
        self,
        session: AsyncSession,
        action_ids: list[int],
        is_rf_skill: bool = True,
        is_other_rf_skill: bool = True,
    ):

        # 构建查询
        query = (
            select(
                *SkillAction.__table__.columns,  # 选择所有 skill_action 字段
                coalesce(AilmentData.ailment_name, "").label("ailment_name"),
                literal(is_rf_skill).label("isRfSkill"),
                literal(is_other_rf_skill).label("isOtherRfSkill"),
            )
            .join(
                AilmentData,
                (SkillAction.action_type == AilmentData.ailment_action)
                & (
                    (SkillAction.action_detail_1 == AilmentData.ailment_detail_1)
                    | (AilmentData.ailment_detail_1 == -1)
                ),
                isouter=True,
            )
            .where(SkillAction.action_id.in_(action_ids))
        )

        result = await session.execute(query)

        if result := result.fetchall():
            return [
                SkillActionData(
                    **dict(zip(SkillActionData.__annotations__.keys(), item))
                )
                for item in result
            ]
        else:
            return []

    @session
    async def get_attack_pattern(
        self, session: AsyncSession, unit_id: int
    ) -> UnitAttackPattern:
        result = await session.execute(
            select(UnitAttackPattern).where(UnitAttackPattern.unit_id == unit_id)
        )
        return result.scalars().all()

    @session
    async def get_spskill_label(self, session: AsyncSession, unit_id: int):
        result = await session.execute(
            select(SpSkillLabelData).where(SpSkillLabelData.unit_id == unit_id)
        )
        return result.scalar_one_or_none()

    @session
    async def get_rf_skill_id(self, session: AsyncSession, skill_id: int):
        result = await session.execute(
            select(UnitSkillDataRF.rf_skill_id).where(
                UnitSkillDataRF.skill_id == skill_id
            )
        )
        return result.scalar_one_or_none()

    @session
    async def get_all_clan_battle_data(
        self, session: AsyncSession, clan_battle_id: int = 0, page: int = 1
    ):
        result = await session.execute(
            select(
                ClanBattle2MapData.clan_battle_id,
                ClanBattleSchedule.release_month,
                ClanBattleSchedule.start_time,
                func.min(ClanBattle2MapData.phase).label("min_phase"),
                func.max(ClanBattle2MapData.phase).label("max_phase"),
                func.group_concat(EnemyParameter.enemy_id, "-").label("enemy_ids"),
                func.group_concat(UnitEnemyData.unit_id, "-").label("unit_ids"),
            )
            .select_from(ClanBattle2MapData)
            .join(
                ClanBattleSchedule,
                ClanBattleSchedule.clan_battle_id == ClanBattle2MapData.clan_battle_id,
                isouter=True,
            )
            .join(
                WaveGroupData,
                WaveGroupData.wave_group_id.in_(
                    [
                        ClanBattle2MapData.wave_group_id_1,
                        ClanBattle2MapData.wave_group_id_2,
                        ClanBattle2MapData.wave_group_id_3,
                        ClanBattle2MapData.wave_group_id_4,
                        ClanBattle2MapData.wave_group_id_5,
                    ]
                ),
                isouter=True,
            )
            .join(
                EnemyParameter,
                WaveGroupData.enemy_id_1 == EnemyParameter.enemy_id,
                isouter=True,
            )
            .join(
                UnitEnemyData,
                EnemyParameter.unit_id == UnitEnemyData.unit_id,
                isouter=True,
            )
            .where(
                or_(
                    ClanBattle2MapData.lap_num_from > 1,
                    ClanBattle2MapData.clan_battle_id < 1011,
                ),
                ClanBattleSchedule.release_month is not None,
                case(
                    (clan_battle_id == 0, 1),
                    else_=(ClanBattle2MapData.clan_battle_id == clan_battle_id),
                )
                == 1,
            )
            .group_by(ClanBattle2MapData.clan_battle_id)
            .order_by(
                ClanBattle2MapData.clan_battle_id.desc(),
                ClanBattle2MapData.lap_num_from,
            )
            .limit(5)
            .offset(page * 5 - 5)  # 分页处理
        )

        if not (result := result.fetchall()):
            return []
        result = [
            ClanBattleData(**dict(zip(ClanBattleData.__annotations__.keys(), item)))
            for item in result
        ]
        for item in result:
            item.end_time = (
                datetime.datetime.strptime(item.start_time, "%Y/%m/%d %H:%M:%S")
                + datetime.timedelta(days=5, hours=-5, seconds=-1)
            ).strftime("%Y/%m/%d %H:%M:%S")
        return result

    @session
    async def get_latest_clan_battle_data(self, session: AsyncSession):
        result = await session.execute(
            select(
                ClanBattle2MapData.clan_battle_id,
                ClanBattleSchedule.release_month,
                ClanBattleSchedule.start_time,
                func.min(ClanBattle2MapData.phase).label("min_phase"),
                func.max(ClanBattle2MapData.phase).label("max_phase"),
                func.group_concat(EnemyParameter.enemy_id, "-").label("enemy_ids"),
                func.group_concat(UnitEnemyData.unit_id, "-").label("unit_ids"),
            )
            .select_from(ClanBattle2MapData)
            .join(
                ClanBattleSchedule,
                ClanBattleSchedule.clan_battle_id == ClanBattle2MapData.clan_battle_id,
                isouter=True,
            )
            .join(
                WaveGroupData,
                WaveGroupData.wave_group_id.in_(
                    [
                        ClanBattle2MapData.wave_group_id_1,
                        ClanBattle2MapData.wave_group_id_2,
                        ClanBattle2MapData.wave_group_id_3,
                        ClanBattle2MapData.wave_group_id_4,
                        ClanBattle2MapData.wave_group_id_5,
                    ]
                ),
                isouter=True,
            )
            .join(
                EnemyParameter,
                WaveGroupData.enemy_id_1 == EnemyParameter.enemy_id,
                isouter=True,
            )
            .join(
                UnitEnemyData,
                EnemyParameter.unit_id == UnitEnemyData.unit_id,
                isouter=True,
            )
            .where(
                or_(
                    ClanBattle2MapData.lap_num_from > 1,
                    ClanBattle2MapData.clan_battle_id < 1011,
                ),
                ClanBattleSchedule.release_month is not None,
            )
            .group_by(ClanBattle2MapData.clan_battle_id)
            .order_by(
                ClanBattle2MapData.clan_battle_id.desc(),
                ClanBattle2MapData.lap_num_from,
            )
            .limit(1)
        )

        if not (result := result.fetchall()):
            return []
        result = [
            ClanBattleData(**dict(zip(ClanBattleData.__annotations__.keys(), item)))
            for item in result
        ]
        for item in result:
            item.end_time = (
                datetime.datetime.strptime(item.start_time, "%Y/%m/%d %H:%M:%S")
                + datetime.timedelta(days=5, hours=-5, seconds=-1)
            ).strftime("%Y/%m/%d %H:%M:%S")
        return result

    @session
    async def get_phase_lap_form_to(
        self, session: AsyncSession, clan_battle_id: int = 0
    ):
        result = await session.execute(
            select(ClanBattle2MapData).where(
                ClanBattle2MapData.clan_battle_id == clan_battle_id
            )
        )
        return result.scalars().all()

    @session
    async def get_all_clan_battle_target_count(
        self, session: AsyncSession, clan_battle_id: int = 0, phase: int = 1
    ):

        enemy_part_ids_expr = func.concat(
            EnemyMParts.child_enemy_parameter_1,
            "-",
            EnemyMParts.child_enemy_parameter_2,
            "-",
            EnemyMParts.child_enemy_parameter_3,
            "-",
            EnemyMParts.child_enemy_parameter_4,
            "-",
            EnemyMParts.child_enemy_parameter_5,
        ).label("enemy_part_ids")

        stmt = (
            select(
                ClanBattle2MapData.clan_battle_id,
                WaveGroupData.enemy_id_1.label("multi_enemy_id"),
                enemy_part_ids_expr,
            )
            .select_from(ClanBattle2MapData)
            .join(
                ClanBattleSchedule,
                ClanBattleSchedule.clan_battle_id == ClanBattle2MapData.clan_battle_id,
                isouter=True,
            )
            .join(
                WaveGroupData,
                WaveGroupData.wave_group_id.in_(
                    [
                        ClanBattle2MapData.wave_group_id_1,
                        ClanBattle2MapData.wave_group_id_2,
                        ClanBattle2MapData.wave_group_id_3,
                        ClanBattle2MapData.wave_group_id_4,
                        ClanBattle2MapData.wave_group_id_5,
                    ]
                ),
                isouter=True,
            )
            .join(
                EnemyMParts,
                WaveGroupData.enemy_id_1 == EnemyMParts.enemy_id,
                isouter=True,
            )
            .where(
                or_(
                    ClanBattle2MapData.lap_num_from > 1,
                    ClanBattle2MapData.clan_battle_id < 1011,
                ),
                enemy_part_ids_expr.isnot(None),
                ClanBattle2MapData.phase == phase,
                case(
                    (clan_battle_id == 0, 1),
                    else_=(ClanBattle2MapData.clan_battle_id == clan_battle_id),
                )
                == 1,
            )
            .group_by(ClanBattle2MapData.clan_battle_id, WaveGroupData.enemy_id_1)
            .order_by(ClanBattle2MapData.clan_battle_id.desc())
        )

        result = await session.execute(stmt)
        if result := result.fetchall():
            return [
                ClanBattleTargetData(
                    **dict(zip(ClanBattleTargetData.__annotations__.keys(), item))
                )
                for item in result
            ]
        else:
            return []

    @session
    async def get_all_events(self, session: AsyncSession, limit: int = 10):
        # 子查询 1：合并 hatsune, shiori 和 seven 的事件记录
        hatsune_sub = select(
            HatsuneSchedule.event_id,
            case(
                (HatsuneSchedule.original_event_id == 0, HatsuneSchedule.event_id),
                else_=HatsuneSchedule.original_event_id,
            ).label("original_event_id"),
            HatsuneSchedule.start_time,
            HatsuneSchedule.end_time,
        )

        shiori_sub = select(
            ShioriEventList.event_id,
            ShioriEventList.original_event_id,
            ShioriEventList.start_time,
            ShioriEventList.end_time,
        )

        seven_sub = select(
            SevenSchedule.event_id,
            SevenSchedule.event_id.label(
                "original_event_id"
            ),  # seven没有original_event_id，使用event_id
            SevenSchedule.start_time,
            SevenSchedule.end_time,
        )

        event_union = union_all(hatsune_sub, shiori_sub, seven_sub).subquery("event")

        # e 子查询
        detail_sub = (
            select(
                EventStoryDetail.story_group_id,
                func.group_concat(EventStoryDetail.reward_id_2, "-").label("unit_ids"),
            )
            .group_by(EventStoryDetail.story_group_id)
            .subquery("e")
        )

        # 主查询

        query = (
            select(
                event_union.c.event_id,
                ((event_union.c.original_event_id % 10000) + 5000).label("story_id"),
                event_union.c.original_event_id,
                event_union.c.start_time,
                event_union.c.end_time,
                func.coalesce(SevenEventSetting.title, EventStoryData.title, "").label(
                    "title"
                ),
                func.coalesce(detail_sub.c.unit_ids, "").label("unit_ids"),
            )
            .outerjoin(
                EventStoryData,
                EventStoryData.story_group_id
                == ((event_union.c.original_event_id % 10000) + 5000),
            )
            .outerjoin(
                SevenEventSetting,
                SevenEventSetting.event_id == event_union.c.event_id,
            )
            .outerjoin(
                detail_sub, detail_sub.c.story_group_id == EventStoryData.story_group_id
            )
            .order_by(
                func.substr(
                    event_union.c.start_time,
                    0,
                    func.instr(event_union.c.start_time, "/"),
                ).desc(),
                func.cast(
                    func.replace(func.substr(event_union.c.start_time, 6, 2), "/", ""),
                    Integer,
                ).desc(),
                func.cast(
                    func.replace(
                        func.substr(
                            event_union.c.start_time,
                            func.instr(event_union.c.start_time, " ") - 2,
                            2,
                        ),
                        "/",
                        "",
                    ),
                    Integer,
                ).desc(),
            )
            .limit(limit)
        )

        result = await session.execute(query)
        if result := result.fetchall():
            return [
                EventData(**dict(zip(EventData.__annotations__.keys(), item)))
                for item in result
            ]
        else:
            return []

    @session
    async def get_drop_event(self, session: AsyncSession, limit: int = 50):

        query = (
            select(
                func.coalesce(
                    func.group_concat(CampaignSchedule.campaign_category, "-"), "0"
                ).label("type"),
                CampaignSchedule.value,
                CampaignSchedule.start_time,
                CampaignSchedule.end_time,
            )
            .where(
                CampaignSchedule.campaign_category.in_(
                    [31, 41, 32, 42, 39, 49, 34, 37, 38, 45]
                ),
                CampaignSchedule.lv_to == -1,
            )
            .group_by(
                CampaignSchedule.start_time,
                CampaignSchedule.end_time,
                CampaignSchedule.value,
            )
            .order_by(CampaignSchedule.id.desc())
            .limit(limit)
        )

        result = await session.execute(query)
        if result := result.fetchall():
            return [
                CalendarEvent(**dict(zip(CalendarEvent.__annotations__.keys(), item)))
                for item in result
            ]
        else:
            return []

    @session
    async def get_mission_event(self, session: AsyncSession, limit: int = 1):

        query = (
            select(
                literal(18).label("type"),
                (MissionRewardData.reward_num * 10).label("value"),
                DailyMissionData.start_time,
                DailyMissionData.end_time,
            )
            .outerjoin(
                MissionRewardData,
                DailyMissionData.mission_reward_id
                == MissionRewardData.mission_reward_id,
            )
            .where(
                MissionRewardData.reward_type == 6, MissionRewardData.reward_num > 100
            )
            .order_by(DailyMissionData.start_time.desc())
            .limit(limit)
        )

        result = await session.execute(query)
        if result := result.fetchall():
            return [
                CalendarEvent(**dict(zip(CalendarEvent.__annotations__.keys(), item)))
                for item in result
            ]
        else:
            return []

    @session
    async def get_login_event(self, session: AsyncSession, limit: int = 1):

        query = (
            select(
                literal(19).label("type"),
                func.sum(LoginBonusDetail.reward_num).label("value"),
                LoginBonusData.start_time,
                LoginBonusData.end_time,
            )
            .outerjoin(
                LoginBonusDetail,
                LoginBonusData.login_bonus_id == LoginBonusDetail.login_bonus_id,
            )
            .where(
                LoginBonusDetail.reward_id == 91002,
                (LoginBonusData.login_bonus_id % 10000) > 2,
            )
            .group_by(LoginBonusData.start_time)
            .order_by(LoginBonusData.start_time.desc())
            .limit(limit)
        )

        result = await session.execute(query)
        if result := result.fetchall():
            return [
                CalendarEvent(**dict(zip(CalendarEvent.__annotations__.keys(), item)))
                for item in result
            ]
        else:
            return []

    @session
    async def get_fortune_event(self, session: AsyncSession, limit: int = 1):

        query = (
            select(
                literal(20).label("type"),
                literal(0).label("value"),
                CharaFortuneSchedule.start_time,
                CharaFortuneSchedule.end_time,
            )
            .order_by(CharaFortuneSchedule.fortune_id.desc())
            .limit(limit)
        )

        result = await session.execute(query)
        if result := result.fetchall():
            return [
                CalendarEvent(**dict(zip(CalendarEvent.__annotations__.keys(), item)))
                for item in result
            ]
        else:
            return []

    @session
    async def get_tower_event(self, session: AsyncSession, limit: int = 1):

        query = (
            select(
                literal(1).label("type"),
                literal(0).label("value"),
                TowerSchedule.start_time,
                TowerSchedule.end_time,
            )
            .order_by(TowerSchedule.tower_schedule_id.desc())
            .limit(limit)
        )

        result = await session.execute(query)
        if result := result.fetchall():
            return [
                CalendarEvent(**dict(zip(CalendarEvent.__annotations__.keys(), item)))
                for item in result
            ]
        else:
            return []

    @session
    async def get_sp_dungeon_event(self, session: AsyncSession, limit: int = 1):

        query = (
            select(
                literal(-1).label("type"),
                literal(0).label("value"),
                SecretDungeonSchedule.start_time,
                SecretDungeonSchedule.end_time,
            )
            .order_by(SecretDungeonSchedule.dungeon_area_id.desc())
            .limit(limit)
        )

        result = await session.execute(query)
        if result := result.fetchall():
            return [
                CalendarEvent(**dict(zip(CalendarEvent.__annotations__.keys(), item)))
                for item in result
            ]
        else:
            return []

    @session
    async def get_fault_event(self, session: AsyncSession, limit: int = 1):

        query = (
            select(
                literal(-2).label("type"),
                literal(0).label("value"),
                TdfSchedule.start_time,
                TdfSchedule.end_time,
            )
            .order_by(TdfSchedule.schedule_id.desc())
            .limit(limit)
        )

        result = await session.execute(query)
        if result := result.fetchall():
            return [
                CalendarEvent(**dict(zip(CalendarEvent.__annotations__.keys(), item)))
                for item in result
            ]
        else:
            return []

    @session
    async def get_abyss_event(self, session: AsyncSession, limit: int = 1):

        query = (
            select(
                literal(-4).label("type"),
                AbyssSchedule.talent_id.label("value"),
                AbyssSchedule.start_time,
                AbyssSchedule.end_time,
            )
            .order_by(AbyssSchedule.abyss_id.desc())
            .limit(limit)
        )
        result = await session.execute(query)
        if result := result.fetchall():
            return [
                CalendarEvent(**dict(zip(CalendarEvent.__annotations__.keys(), item)))
                for item in result
            ]
        else:
            return []

    @session
    async def get_free_gacha_event(self, session: AsyncSession, limit: int = 1):
        a = alias(CampaignFreegacha)
        b = alias(CampaignFreegacha)

        query = (
            select(
                a.c.id.label("id"),
                func.coalesce(b.c.relation_count, 0).label("max_count"),
                a.c.start_time,
                case(
                    (b.c.end_time.is_not(None), b.c.end_time), else_=a.c.end_time
                ).label("end_time"),
            )
            .outerjoin(b, a.c.campaign_id == b.c.relation_id)
            .where(a.c.freegacha_10 == 1)
            .order_by(a.c.start_time.desc())
            .limit(limit)
        )

        result = await session.execute(query)
        if result := result.fetchall():
            return [
                CampaignFreegachaData(
                    **dict(zip(CampaignFreegachaData.__annotations__.keys(), item))
                )
                for item in result
            ]
        else:
            return []

    @session
    async def get_dome_event(self, session: AsyncSession, limit: int = 1):
        try:
            query = (
                select(
                    literal(-3).label("type"),
                    literal(0).label("value"),
                    DomeScheduleData.start_time,
                    DomeScheduleData.end_time,
                )
                .order_by(DomeScheduleData.schedule_id.desc())
                .limit(limit)
            )

            result = await session.execute(query)
        except Exception as e:
            query = (
                select(
                    literal(-3).label("type"),
                    literal(0).label("value"),
                    ColosseumScheduleData.start_time,
                    ColosseumScheduleData.end_time,
                )
                .order_by(ColosseumScheduleData.schedule_id.desc())
                .limit(limit)
            )
            result = await session.execute(query)
        if result := result.fetchall():
            return [
                CalendarEvent(**dict(zip(CalendarEvent.__annotations__.keys(), item)))
                for item in result
            ]
        else:
            return []

    @session
    async def get_birthday_list(
        self,
        session: AsyncSession,
        start_timestamp: int,
        after_days: int = 7,
        max_unit_id: int = 9999999,
    ):
        start_date = datetime.datetime.fromtimestamp(start_timestamp)

        valid_md_pairs = [
            (d.month, d.day)
            for d in (
                start_date + datetime.timedelta(days=i) for i in range(after_days)
            )
        ]

        # CASE 表达式处理异常值
        birth_month_case = (
            case(
                (
                    (UnitProfile.birth_month.like("%-%"))
                    | (UnitProfile.birth_month.like("%?%"))
                    | (UnitProfile.birth_month.like("%？%"))
                    | (UnitProfile.birth_month == 0),
                    999,
                ),
                else_=UnitProfile.birth_month,
            )
            .cast(Integer)
            .label("birth_month_int")
        )

        birth_day_case = (
            case(
                (
                    (UnitProfile.birth_day.like("%-%"))
                    | (UnitProfile.birth_day.like("%?%"))
                    | (UnitProfile.birth_day.like("%？%"))
                    | (UnitProfile.birth_day == 0),
                    999,
                ),
                else_=UnitProfile.birth_day,
            )
            .cast(Integer)
            .label("birth_day_int")
        )

        query = (
            select(
                birth_month_case,
                birth_day_case,
                func.group_concat(UnitData.unit_id, "-").label("unit_ids"),
                func.group_concat(UnitData.unit_name, "-").label("unit_names"),
            )
            .outerjoin(UnitData, UnitProfile.unit_id == UnitData.unit_id)
            .where(
                UnitData.unit_id < max_unit_id,
                UnitData.search_area_width > 0,
                tuple_(birth_month_case, birth_day_case).in_(valid_md_pairs),
            )
            .group_by(birth_month_case, birth_day_case)
            .order_by(birth_month_case, birth_day_case)
        )
        result = await session.execute(query)
        if result := result.fetchall():
            return [
                BirthdayData(**dict(zip(BirthdayData.__annotations__.keys(), item)))
                for item in result
            ]
        else:
            return []

    @session
    async def get_gacha_history(self, session: AsyncSession, limit: int = 200):
        query = (
            select(
                GachaData.gacha_id,
                GachaData.gacha_name,
                func.coalesce(func.group_concat(GachaExchangeLineup.id, "-"), "").label(
                    "ids"
                ),
                func.coalesce(
                    func.group_concat(GachaExchangeLineup.unit_id, "-"), ""
                ).label("unit_ids"),
                func.coalesce(func.group_concat(UnitData.unit_name, "-"), "").label(
                    "unit_names"
                ),
                func.coalesce(func.group_concat(UnitData.is_limited, "-"), "").label(
                    "is_limiteds"
                ),
                func.coalesce(
                    func.group_concat(GachaExchangeLineup.gacha_bonus_id, "-"), ""
                ).label("is_ups"),
                GachaData.description,
                GachaData.start_time,
                GachaData.end_time,
            )
            .outerjoin(
                GachaExchangeLineup,
                GachaData.exchange_id == GachaExchangeLineup.exchange_id,
            )
            .outerjoin(UnitData, GachaExchangeLineup.unit_id == UnitData.unit_id)
            .filter(
                ~GachaData.gacha_id.like("1%"),
                ~GachaData.gacha_id.like("2%"),
                GachaData.gacha_id < 60001,
            )
            .group_by(GachaData.gacha_id)
            .order_by(GachaData.start_time.desc())
            .limit(limit)
        )

        result = await session.execute(query)
        if result := result.fetchall():
            return [
                GachaHistoryData(
                    **dict(zip(GachaHistoryData.__annotations__.keys(), item))
                )
                for item in result
            ]
        else:
            return []

    @session
    async def get_fes_unit_id_list(self, session: AsyncSession):
        query = (
            select(
                func.coalesce(
                    func.group_concat(GachaExchangeLineup.unit_id, "-"), ""
                ).label("unit_ids"),
            )
            .select_from(GachaData)
            .outerjoin(
                GachaExchangeLineup,
                GachaData.exchange_id == GachaExchangeLineup.exchange_id,
            )
            .outerjoin(UnitData, GachaExchangeLineup.unit_id == UnitData.unit_id)
            .filter(GachaData.gacha_id.like("5%"))
            .group_by(GachaData.gacha_id)
            .order_by(GachaData.exchange_id.desc())
            .limit(1)
        )
        result = await session.execute(query)
        return result.unit_ids.split("-") if (result := result.first()) else []

    @staticmethod
    def _merge_table_row_count_sync(
        conn: sqlite3.Connection, schema: str, table: str
    ) -> int:
        return conn.execute(f'SELECT COUNT(*) FROM "{schema}"."{table}"').fetchone()[0]

    @staticmethod
    def _merge_list_user_tables_sync(
        conn: sqlite3.Connection, schema: str = "main"
    ) -> List[str]:
        master = "sqlite_master" if schema == "main" else f"{schema}.sqlite_master"
        rows = conn.execute(
            f"SELECT name FROM {master} WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ).fetchall()
        return [name for (name,) in rows]

    @classmethod
    def merge_supplement_sync(
        cls, jp_path: Union[str, Path], supplement_path: Union[str, Path]
    ) -> List[Tuple[str, int, int]]:
        jp_path = Path(jp_path)
        supplement_path = Path(supplement_path).resolve()
        if not jp_path.exists():
            raise FileNotFoundError(f"日服数据库不存在: {jp_path}")
        if not supplement_path.exists():
            raise FileNotFoundError(f"补充库不存在: {supplement_path}")

        conn = sqlite3.connect(jp_path)
        merged: List[Tuple[str, int, int]] = []
        try:
            conn.execute("PRAGMA busy_timeout = 30000")
            conn.execute("ATTACH DATABASE ? AS sup", (str(supplement_path),))
            jp_tables = set(cls._merge_list_user_tables_sync(conn, "main"))
            for table in cls._merge_list_user_tables_sync(conn, "sup"):
                sup_count = cls._merge_table_row_count_sync(conn, "sup", table)
                jp_count = (
                    cls._merge_table_row_count_sync(conn, "main", table)
                    if table in jp_tables
                    else 0
                )
                if sup_count <= jp_count:
                    continue

                create_sql = conn.execute(
                    "SELECT sql FROM sup.sqlite_master WHERE type='table' AND name=?",
                    (table,),
                ).fetchone()[0]
                conn.execute(f'DROP TABLE IF EXISTS main."{table}"')
                conn.execute(create_sql)
                conn.execute(f'INSERT INTO main."{table}" SELECT * FROM sup."{table}"')
                merged.append((table, jp_count, sup_count))
                logger.info(f"合并表 {table}: {jp_count} -> {sup_count}")

            conn.commit()
        finally:
            conn.close()

        logger.info(f"日服补充库合并完成，共 {len(merged)} 张表")
        return merged

    async def merge_supplement(
        self, supplement_path: Union[str, Path]
    ) -> List[Tuple[str, int, int]]:
        """将补充库中比当前库行数更多的表合并进来。"""
        await self.engine.dispose()
        return await asyncio.to_thread(
            self.merge_supplement_sync, self.db_path, supplement_path
        )


async def merge_supplement_db(
    jp_path: Union[str, Path], supplement_path: Union[str, Path]
) -> List[Tuple[str, int, int]]:
    return await asyncio.to_thread(
        PCRDatabase.merge_supplement_sync, jp_path, supplement_path
    )


cn_data = PCRDatabase(FilePath.cn_db.value)
jp_data = PCRDatabase(FilePath.jp_db.value)
tw_data = PCRDatabase(FilePath.tw_db.value)


if __name__ == "__main__":
    import asyncio

    async def _main():
        await jp_data.merge_supplement(FilePath.jp_supplement_db.value)
        await jp_data.engine.dispose()

    asyncio.run(_main())
