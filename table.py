from typing import Optional
from sqlmodel import Column, Float, SQLModel, Field

from sqlalchemy.orm import registry


class PCRModel(SQLModel, registry=registry()):
    pass


class RedeemUnit(PCRModel, table=True):
    __tablename__ = "redeem_unit"
    id: int = Field(default=None, primary_key=True)
    unit_id: int = Field(index=True)
    slot_id: int
    condition_category: int
    condition_id: int
    consume_num: str


class UnitData(PCRModel, table=True):
    __tablename__ = "unit_data"
    unit_id: int = Field(primary_key=True)
    unit_name: str
    kana: Optional[str] = None
    prefab_id: Optional[int] = None
    prefab_id_battle: Optional[int] = None
    is_limited: Optional[int] = None
    rarity: Optional[int] = None
    motion_type: Optional[int] = None
    se_type: Optional[int] = None
    move_speed: Optional[int] = None
    search_area_width: Optional[int] = None
    atk_type: Optional[int] = None
    normal_atk_cast_time: Optional[float] = None
    cutin_1: Optional[int] = None
    cutin_2: Optional[int] = None
    cutin1_star6: Optional[int] = None
    cutin2_star6: Optional[int] = None
    guild_id: Optional[int] = None
    exskill_display: Optional[int] = None
    comment: Optional[str] = None
    only_disp_owned: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    original_unit_id: Optional[int] = None


class UnitProfile(PCRModel, table=True):
    __tablename__ = "unit_profile"
    unit_id: int = Field(primary_key=True)
    unit_name: str
    age: Optional[str] = None
    guild: Optional[str] = None
    race: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    birth_month: Optional[str] = None
    birth_day: Optional[str] = None
    blood_type: Optional[str] = None
    favorite: Optional[str] = None
    voice: Optional[str] = None
    voice_id: Optional[int] = None
    catch_copy: Optional[str] = None
    self_text: Optional[str] = None
    guild_id: Optional[str] = None


class ActualUnitBackground(PCRModel, table=True):
    __tablename__ = "actual_unit_background"
    unit_id: int = Field(primary_key=True)
    unit_name: Optional[str] = None
    bg_id: Optional[int] = None
    face_type: Optional[int] = None


class UnitUniqueEquipment(PCRModel, table=True):
    __tablename__ = "unit_unique_equipment"
    unit_id: int = Field(primary_key=True)
    equip_slot: int = Field(primary_key=True)
    equip_id: int


class UnitUniqueEquip(PCRModel, table=True):
    __tablename__ = "unit_unique_equip"
    unit_id: int = Field(primary_key=True)
    equip_slot: int = Field(primary_key=True)
    equip_id: int


class UniqueEquipEnhanceRate(PCRModel, table=True):
    __tablename__ = "unique_equip_enhance_rate"
    id: int = Field(primary_key=True)
    equipment_id: int
    min_lv: int
    max_lv: int
    hp: float
    atk: float
    magic_str: float
    def_: float = Field(sa_column=Column("def", Float))
    magic_def: float
    physical_critical: float
    magic_critical: float
    wave_hp_recovery: float
    wave_energy_recovery: float
    dodge: float
    physical_penetrate: float
    magic_penetrate: float
    life_steal: float
    hp_recovery_rate: float
    energy_recovery_rate: float
    energy_reduce_rate: float
    accuracy: float


class UniqueEquipmentEnhanceRate(PCRModel, table=True):
    __tablename__ = "unique_equipment_enhance_rate"
    equipment_id: int = Field(primary_key=True)
    equipment_name: str
    description: str
    promotion_level: int
    hp: float
    atk: float
    magic_str: float
    def_: float = Field(sa_column=Column("def", Float))
    magic_def: float
    physical_critical: float
    magic_critical: float
    wave_hp_recovery: float
    wave_energy_recovery: float
    dodge: float
    physical_penetrate: float
    magic_penetrate: float
    life_steal: float
    hp_recovery_rate: float
    energy_recovery_rate: float
    energy_reduce_rate: float
    accuracy: float


class UniqueEquipmentData(PCRModel, table=True):
    __tablename__ = "unique_equipment_data"
    equipment_id: int = Field(primary_key=True, nullable=False)
    equipment_name: str
    description: str
    promotion_level: int
    craft_flg: int
    equipment_enhance_point: int
    sale_price: int
    require_level: int
    hp: float
    atk: float
    magic_str: float
    def_: float = Field(sa_column=Column("def", Float))
    magic_def: float
    physical_critical: float
    magic_critical: float
    wave_hp_recovery: float
    wave_energy_recovery: float
    dodge: float
    physical_penetrate: float
    magic_penetrate: float
    life_steal: float
    hp_recovery_rate: float
    energy_recovery_rate: float
    energy_reduce_rate: float
    enable_donation: Optional[int] = None
    accuracy: Optional[float] = None


class UniqueEquipmentEnhanceData(PCRModel, table=True):
    __tablename__ = "unique_equipment_enhance_data"
    equip_slot: int = Field(primary_key=True, nullable=False)  # 主键1
    enhance_level: int = Field(primary_key=True, nullable=False)  # 主键2
    needed_point: int
    total_point: int
    needed_mana: int
    rank: int


class CharaStoryStatus(PCRModel, table=True):
    __tablename__ = "chara_story_status"

    story_id: int = Field(primary_key=True, nullable=False)  # 主键

    unlock_story_name: str

    # 角色属性状态类型和比率
    status_type_1: int
    status_rate_1: int
    status_type_2: int
    status_rate_2: int
    status_type_3: int
    status_rate_3: int
    status_type_4: int
    status_rate_4: int
    status_type_5: int
    status_rate_5: int

    # 角色ID列表（最多20个）
    chara_id_1: int
    chara_id_2: int
    chara_id_3: int
    chara_id_4: int
    chara_id_5: int
    chara_id_6: int
    chara_id_7: int
    chara_id_8: int
    chara_id_9: int
    chara_id_10: int
    chara_id_11: int
    chara_id_12: int
    chara_id_13: int
    chara_id_14: int
    chara_id_15: int
    chara_id_16: int
    chara_id_17: int
    chara_id_18: int
    chara_id_19: int
    chara_id_20: int


class CharaIdentity(PCRModel, table=True):
    __tablename__ = "chara_identity"
    unit_id: int = Field(primary_key=True, nullable=False)  # 角色唯一 ID（主键）
    chara_type: int
    chara_type_2: int
    chara_type_3: int


class StoryDetail(PCRModel, table=True):
    __tablename__ = "story_detail"
    story_id: int = Field(primary_key=True, nullable=False)  # 主键
    story_group_id: Optional[int] = None
    title: str
    sub_title: Optional[str] = None
    visible_type: int
    story_end: int
    pre_story_id: Optional[int] = None
    force_unlock_time: Optional[str] = None
    pre_story_id_2: Optional[int] = None
    force_unlock_time_2: Optional[str] = None
    love_level: Optional[int] = None
    requirement_id: Optional[int] = None
    unlock_quest_id: Optional[int] = None
    story_quest_id: Optional[int] = None
    lock_all_text: Optional[int] = None
    reward_type_1: Optional[int] = None
    reward_id_1: Optional[int] = None
    reward_value_1: Optional[int] = None
    reward_type_2: Optional[int] = None
    reward_id_2: Optional[int] = None
    reward_value_2: Optional[int] = None
    reward_type_3: Optional[int] = None
    reward_id_3: Optional[int] = None
    reward_value_3: Optional[int] = None
    start_time: Optional[str] = None  # 额外字段
    end_time: Optional[str] = None  # 额外字段


class UnitSkillData(PCRModel, table=True):
    __tablename__ = "unit_skill_data"

    unit_id: int = Field(primary_key=True, nullable=False)  # 主键

    union_burst: int
    sp_union_burst: int
    union_burst_evolution: int

    # 主技能 (Main Skills)
    main_skill_1: int
    main_skill_2: int
    main_skill_3: int
    main_skill_4: int
    main_skill_5: int
    main_skill_6: int
    main_skill_7: int
    main_skill_8: int
    main_skill_9: int
    main_skill_10: int

    # 主技能进化 (Main Skill Evolutions)
    main_skill_evolution_1: int
    main_skill_evolution_2: int

    # EX 技能 (EX Skills)
    ex_skill_1: int
    ex_skill_2: int
    ex_skill_3: int
    ex_skill_4: int
    ex_skill_5: int

    # EX 技能进化 (EX Skill Evolutions)
    ex_skill_evolution_1: int
    ex_skill_evolution_2: int
    ex_skill_evolution_3: int
    ex_skill_evolution_4: int
    ex_skill_evolution_5: int

    # SP 技能 (Special Skills)
    sp_skill_1: int
    sp_skill_2: int
    sp_skill_3: int
    sp_skill_4: int
    sp_skill_5: int

    # SP 技能进化 (Special Skill Evolutions)
    sp_skill_evolution_1: int
    sp_skill_evolution_2: int


class SkillData(PCRModel, table=True):
    __tablename__ = "skill_data"

    skill_id: int = Field(primary_key=True, nullable=False)  # 主键
    name: Optional[str] = None
    skill_type: int
    skill_area_width: int
    skill_cast_time: float
    boss_ub_cool_time: float

    # 技能动作
    action_1: Optional[int] = None
    action_2: Optional[int] = None
    action_3: Optional[int] = None
    action_4: Optional[int] = None
    action_5: Optional[int] = None
    action_6: Optional[int] = None
    action_7: Optional[int] = None
    action_8: Optional[int] = None
    action_9: Optional[int] = None
    action_10: Optional[int] = None

    # 依赖技能动作
    depend_action_1: Optional[int] = None
    depend_action_2: Optional[int] = None
    depend_action_3: Optional[int] = None
    depend_action_4: Optional[int] = None
    depend_action_5: Optional[int] = None
    depend_action_6: Optional[int] = None
    depend_action_7: Optional[int] = None
    depend_action_8: Optional[int] = None
    depend_action_9: Optional[int] = None
    depend_action_10: Optional[int] = None

    # 额外字段
    description: Optional[str] = None
    icon_type: Optional[int] = None


class SkillAction(PCRModel, table=True):
    __tablename__ = "skill_action"

    action_id: int = Field(primary_key=True, nullable=False)  # 主键
    class_id: int
    action_type: int
    action_detail_1: int
    action_detail_2: int
    action_detail_3: int

    # 行动数值参数
    action_value_1: float
    action_value_2: float
    action_value_3: float
    action_value_4: float
    action_value_5: float
    action_value_6: float
    action_value_7: float

    # 目标相关字段
    target_assignment: int
    target_area: int
    target_range: int
    target_type: int
    target_number: int
    target_count: int

    # 额外描述信息
    description: Optional[str] = None
    level_up_disp: Optional[str] = None


class AilmentData(PCRModel, table=True):
    __tablename__ = "ailment_data"
    ailment_id: int = Field(primary_key=True, nullable=False)  # 主键
    ailment_action: int
    ailment_detail_1: int
    ailment_name: Optional[str] = None  # 可能为空的文本字段


class UnitAttackPattern(PCRModel, table=True):
    __tablename__ = "unit_attack_pattern"

    pattern_id: int = Field(primary_key=True, nullable=False)  # 主键
    unit_id: int
    loop_start: int
    loop_end: int

    # 攻击模式（最多20个）
    atk_pattern_1: int
    atk_pattern_2: int
    atk_pattern_3: int
    atk_pattern_4: int
    atk_pattern_5: int
    atk_pattern_6: int
    atk_pattern_7: int
    atk_pattern_8: int
    atk_pattern_9: int
    atk_pattern_10: int
    atk_pattern_11: int
    atk_pattern_12: int
    atk_pattern_13: int
    atk_pattern_14: int
    atk_pattern_15: int
    atk_pattern_16: int
    atk_pattern_17: int
    atk_pattern_18: int
    atk_pattern_19: int
    atk_pattern_20: int


class SpSkillLabelData(PCRModel, table=True):
    __tablename__ = "sp_skill_label"
    unit_id: int = Field(primary_key=True, nullable=False)  # 主键
    normal_label_text: Optional[str] = None  # 普通技能标签
    sp_label_text: Optional[str] = None  # SP 技能标签


class UnitSkillDataRF(PCRModel, table=True):
    __tablename__ = "unit_skill_data_rf"
    id: int = Field(primary_key=True, nullable=False)  # 主键
    skill_id: int  # 关联的技能 ID
    rf_skill_id: int  # RF 版本技能 ID
    min_lv: int  # 最低适用等级
    max_lv: int  # 最高适用等级


class UnitEnemyData(PCRModel, table=True):
    __tablename__ = "unit_enemy_data"
    unit_id: int = Field(primary_key=True)
    unit_name: str
    prefab_id: int
    motion_type: int
    se_type: int
    move_speed: int
    search_area_width: int
    atk_type: int
    normal_atk_cast_time: float
    cutin: int
    cutin_star6: int
    visual_change_flag: int
    comment: str


class WaveGroupData(PCRModel, table=True):
    __tablename__ = "wave_group_data"
    id: int = Field(primary_key=True)
    wave_group_id: int
    odds: int

    enemy_id_1: int
    drop_gold_1: int
    drop_reward_id_1: int

    enemy_id_2: int
    drop_gold_3: int
    drop_reward_id_2: int

    enemy_id_3: int
    drop_gold_2: int
    drop_reward_id_3: int

    enemy_id_4: int
    drop_gold_4: int
    drop_reward_id_4: int

    enemy_id_5: int
    drop_gold_5: int
    drop_reward_id_5: int

    guest_enemy_id: int
    guest_lane: int


class EnemyParameter(PCRModel, table=True):
    __tablename__ = "enemy_parameter"
    enemy_id: int = Field(primary_key=True)
    unit_id: int
    name: str
    level: int
    rarity: int
    promotion_level: int
    hp: int
    atk: int
    magic_str: int
    def_: float = Field(sa_column=Column("def", Float))
    magic_def: int
    physical_critical: int
    magic_critical: int
    wave_hp_recovery: int
    wave_energy_recovery: int
    dodge: int
    physical_penetrate: int
    magic_penetrate: int
    life_steal: int
    hp_recovery_rate: int
    energy_recovery_rate: int
    energy_reduce_rate: int
    union_burst_level: int
    main_skill_lv_1: int
    main_skill_lv_2: int
    main_skill_lv_3: int
    main_skill_lv_4: int
    main_skill_lv_5: int
    main_skill_lv_6: int
    main_skill_lv_7: int
    main_skill_lv_8: int
    main_skill_lv_9: int
    main_skill_lv_10: int
    ex_skill_lv_1: int
    ex_skill_lv_2: int
    ex_skill_lv_3: int
    ex_skill_lv_4: int
    ex_skill_lv_5: int
    resist_status_id: int
    resist_variation_id: int
    accuracy: int
    break_durability: int
    unique_equipment_flag_1: int
    virtual_hp: int


class ClanBattleSchedule(PCRModel, table=True):
    __tablename__ = "clan_battle_schedule"
    clan_battle_id: int = Field(primary_key=True)
    release_month: int
    last_clan_battle_id: int
    point_per_stamina: int
    cost_group_id: int
    cost_group_id_s: int
    map_bgm: str
    resource_id: int
    start_time: str
    end_time: str
    mode_change_start_time: str
    mode_change_end_time: str
    mode_change_remind_time: str


class ClanBattle2MapData(PCRModel, table=True):
    __tablename__ = "clan_battle_2_map_data"
    id: int = Field(primary_key=True)
    clan_battle_id: int
    map_bg: int
    difficulty: int
    lap_num_from: int
    lap_num_to: int
    boss_id_1: int
    boss_id_2: int
    boss_id_3: int
    boss_id_4: int
    boss_id_5: int
    aura_effect: int
    rsl_unlock_lap: int
    phase: int
    wave_group_id_1: int
    wave_group_id_2: int
    wave_group_id_3: int
    wave_group_id_4: int
    wave_group_id_5: int
    fix_reward_id_1: int
    fix_reward_id_2: int
    fix_reward_id_3: int
    fix_reward_id_4: int
    fix_reward_id_5: int
    damage_rank_id_1: int
    damage_rank_id_2: int
    damage_rank_id_3: int
    damage_rank_id_4: int
    damage_rank_id_5: int
    reward_gold_coefficient: float
    limited_mana: Optional[int] = None  # 唯一可为 null 字段
    last_attack_reward_id: int
    score_coefficient_1: float
    score_coefficient_2: float
    score_coefficient_3: float
    score_coefficient_4: float
    score_coefficient_5: float
    param_adjust_id: int
    param_adjust_interval: int


class EnemyMParts(PCRModel, table=True):
    __tablename__ = "enemy_m_parts"
    enemy_id: int = Field(primary_key=True)
    name: str
    child_enemy_parameter_1: int
    child_enemy_parameter_2: int
    child_enemy_parameter_3: int
    child_enemy_parameter_4: int
    child_enemy_parameter_5: int


class CampaignFreegacha(PCRModel, table=True):
    __tablename__ = "campaign_freegacha"

    id: int = Field(primary_key=True)
    campaign_id: int
    freegacha_1: int
    freegacha_10: int
    start_time: str
    end_time: str
    stock_10_flag: int
    relation_id: int
    relation_count: int


class CampaignSchedule(PCRModel, table=True):
    __tablename__ = "campaign_schedule"

    id: int = Field(primary_key=True)
    campaign_category: int
    value: float
    system_id: int
    icon_image: int
    lv_from: int
    lv_to: int
    start_time: str
    end_time: str
    level_id: int
    shiori_group_id: int
    duplication_order: int
    beginner_id: int
    campaign_type: int


class CharaFortuneSchedule(PCRModel, table=True):
    __tablename__ = "chara_fortune_schedule"

    fortune_id: int = Field(primary_key=True)
    name: str
    start_time: str
    end_time: str


class ColosseumScheduleData(PCRModel, table=True):
    __tablename__ = "colosseum_schedule_data"

    schedule_id: int = Field(primary_key=True)
    start_time: str
    count_start_time: str
    end_time: str
    close_time: str
    calc_start: str
    result_start: str


class HatsuneSchedule(PCRModel, table=True):
    __tablename__ = "hatsune_schedule"

    event_id: int = Field(primary_key=True)
    teaser_time: str
    start_time: str
    end_time: str
    close_time: str
    background: int
    sheet_id: str
    que_id: str
    banner_unit_id: int
    count_start_time: str
    backgroud_size_x: int
    backgroud_size_y: int
    backgroud_pos_x: int
    backgroud_pos_y: int
    original_event_id: int
    series_event_id: int
    teaser_dialog_type: int


class SecretDungeonSchedule(PCRModel, table=True):
    __tablename__ = "secret_dungeon_schedule"

    dungeon_area_id: int = Field(primary_key=True)
    teaser_time: str
    start_time: str
    count_start_time: str
    end_time: str
    close_time: str


class TdfSchedule(PCRModel, table=True):
    __tablename__ = "tdf_schedule"

    schedule_id: int = Field(primary_key=True)
    count_start_time: str
    recovery_disable_time: str
    start_time: str
    end_time: str
    ex_quest_id: int


class TowerSchedule(PCRModel, table=True):
    __tablename__ = "tower_schedule"

    tower_schedule_id: int = Field(primary_key=True)
    max_tower_area_id: int
    opening_story_id: int
    count_start_time: str
    recovery_disable_time: str
    start_time: str
    end_time: str


class ShioriEventList(PCRModel, table=True):
    __tablename__ = "shiori_event_list"

    event_id: int = Field(primary_key=True)
    start_time: str
    end_time: str
    banner_y: int
    condition_story_id: int
    condition_chara_id: int
    condition_main_quest_id: int
    condition_shiori_quest_id: int
    original_event_id: int
    series_event_id: int
    original_start_time: str
    gojuon_order: int
    help_index: str


class EventStoryDetail(PCRModel, table=True):
    __tablename__ = "event_story_detail"

    story_id: int = Field(primary_key=True)
    story_group_id: int
    title: str
    sub_title: str
    visible_type: int
    story_end: int
    pre_story_id: int
    pre_story_id_2: int
    love_level: int
    requirement_id: int
    unlock_quest_id: int
    story_quest_id: int
    lock_all_text: int
    can_bookmark: int
    reward_type_1: int
    reward_id_1: int
    reward_value_1: int
    reward_type_2: int
    reward_id_2: int
    reward_value_2: int
    reward_type_3: int
    reward_id_3: int
    reward_value_3: int
    start_time: str
    end_time: str


class EventStoryData(PCRModel, table=True):
    __tablename__ = "event_story_data"

    story_group_id: int = Field(primary_key=True)
    story_type: int
    value: int
    title: str
    thumbnail_id: int
    disp_order: int
    start_time: str
    end_time: str


class DailyMissionData(PCRModel, table=True):
    __tablename__ = "daily_mission_data"

    daily_mission_id: int = Field(primary_key=True)
    disp_group: int
    category_icon: int
    description: str
    mission_condition: int
    condition_num: int
    mission_reward_id: int
    start_time: str
    end_time: str
    min_level: int
    max_level: int
    title_color_id: int
    visible_flag: int
    condition_value_1: Optional[int]
    condition_value_2: Optional[int]
    condition_value_3: Optional[int]
    system_id: Optional[int]


class MissionRewardData(PCRModel, table=True):
    __tablename__ = "mission_reward_data"

    id: int = Field(primary_key=True)
    mission_reward_id: int
    reward_type: int
    reward_num: int
    lv_from: int
    lv_to: int
    start_time: str
    end_time: str
    reward_id: Optional[int]


class LoginBonusData(PCRModel, table=True):
    __tablename__ = "login_bonus_data"

    login_bonus_id: int = Field(primary_key=True)
    name: str
    login_bonus_type: int
    count_num: int
    start_time: str
    end_time: str
    bg_id: int
    stamp_id: int
    odds_group_id: int
    adv_play_type: int
    count_type: int


class LoginBonusDetail(PCRModel, table=True):
    __tablename__ = "login_bonus_detail"

    id: int = Field(primary_key=True)
    login_bonus_id: int
    count: int
    reward_type: int
    reward_id: int
    reward_num: int
    character_id: int
    character_name: str
    description: str
    voice_id: int
    bg_id: int


class GachaData(PCRModel, table=True):
    __tablename__ = "gacha_data"
    gacha_id: int = Field(primary_key=True)
    gacha_name: str
    pick_up_chara_text: Optional[str] = None
    description: Optional[str] = None
    description_2: Optional[str] = None
    description_sp: Optional[str] = None
    unknown_1: Optional[str] = None
    unknown_2: int
    parallel_id: int
    pickup_badge: int
    gacha_detail: Optional[str] = None
    gacha_cost_type: int
    price: int
    free_gacha_type: int
    free_gacha_interval_time: int
    free_gacha_count: int
    discount_price: int
    gacha_odds: Optional[str] = None
    gacha_odds_star2: Optional[str] = None
    gacha_type: int
    movie_id: int
    start_time: str
    end_time: str
    ticket_id: int
    special_id: Optional[int] = None
    exchange_id: int
    ticket_id_10: Optional[int] = None
    rarity_odds: Optional[str] = None
    chara_odds_star1: Optional[str] = None
    chara_odds_star2: Optional[str] = None
    chara_odds_star3: Optional[str] = None
    gacha10_special_odds_star1: Optional[str] = None
    gacha10_special_odds_star2: Optional[str] = None
    gacha10_special_odds_star3: Optional[str] = None
    prizegacha_id: Optional[int] = None
    gacha_bonus_id: Optional[int] = None
    gacha_times_limit10: Optional[int] = None
    pickup_id: Optional[int] = None


class GachaExchangeLineup(PCRModel, table=True):
    __tablename__ = "gacha_exchange_lineup"
    id: int = Field(primary_key=True)
    exchange_id: int
    unit_id: int
    rarity: int
    gacha_bonus_id: int
    start_time: str
    end_time: str
