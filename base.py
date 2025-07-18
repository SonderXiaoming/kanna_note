from pathlib import Path
from enum import Enum


class FilePath(Enum):
    base = Path(__file__).parent / "resource"

    data = base / "data"
    cn_db = data / "pcr_cn.db"
    tw_db = data / "pcr_tw.db"
    jp_db = data / "pcr_jp.db"
    temp_db = data / "temp.db"

    img = base / "img"
    icon = img / "icon"
    skill_icon = img / "skill_icon"
    fullcard = img / "fullcard"
    equipment = img / "equipment"
    enemy = img / "enemy"
    teaser = img / "teaser"

    font = base / "font"
    font_fz = str(font / "方正综艺简体.ttf")
    font_ms_regular = str(font / "Microsoft-YaHei-Regular.ttc")
    font_ms_bold = str(font / "Microsoft-YaHei-Bold.ttc")
    font_jp = str(font / "A-OTF-GothicMB101Pro-DeBold-2.otf")


class FetchUrl(Enum):
    jp_url = "https://wthee.xyz/db/redive_jp.db.br"
    tw_url = "https://wthee.xyz/db/redive_tw.db.br"
    cn_url = "https://wthee.xyz/db/redive_cn.db.br"
    fullcard_url = "https://redive.estertion.win/card/full/"
    skill_icon_url = "https://redive.estertion.win/icon/skill/"
    equipment_url = "https://redive.estertion.win/icon/equipment/"
    enemy_icon_url = "https://redive.estertion.win/icon/unit/"
    teaser_url = "https://wthee.xyz/redive/{}/resource/event/teaser/"


class GameSetting(Enum):
    other_limit_level = 300
    tp_limit_level = 260


SKILL_DESCRIPTIONS = {
    0: "none",
    1: "skill_type_1",
    2: "skill_type_2",
    3: "none",
    4: "skill_type_4_5",
    5: "skill_type_4_5",
    6: "skill_type_6",
    7: "none",
    8: "none",
    9: "none",
    10: "none",
    11: "none",
    12: "skill_type_12",
    13: "skill_type_13",
    14: "skill_type_14",
    15: "skill_type_15",
    16: "skill_type_16_92",
    17: "skill_type_17",
    18: "skill_type_18_19",
    19: "skill_type_18_19",
    20: "skill_type_20",
    21: "skill_type_21",
    22: "skill_type_22",
    23: "none",
    24: "skill_type_24",
    25: "none",
    26: "none",
    27: "none",
    28: "none",
    29: "none",
    30: "skill_type_30",
    31: "none",
    32: "skill_type_32",
    33: "skill_type_33",
    34: "skill_type_34",
    102: "skill_type_34",
    35: "skill_type_35_43_60_77",
    101: "skill_type_35_43_60_77",
    36: "skill_type_36_37_38_39_40",
    37: "skill_type_36_37_38_39_40",
    38: "skill_type_36_37_38_39_40",
    39: "skill_type_36_37_38_39_40",
    40: "skill_type_36_37_38_39_40",
    41: "none",
    42: "skill_type_42",
    43: "skill_type_35_43_60_77",
    44: "skill_type_44",
    45: "none",
    46: "skill_type_46",
    47: "none",
    48: "skill_type_48",
    49: "skill_type_49",
    50: "skill_type_50",
    51: "none",
    52: "none",
    53: "none",
    54: "skill_type_54",
    55: "none",
    56: "skill_type_56",
    57: "skill_type_57",
    58: "skill_type_58",
    59: "skill_type_59",
    60: "skill_type_35_43_60_77",
    61: "skill_type_61",
    62: "skill_type_62",
    63: "skill_type_63",
    69: "skill_type_69",
    70: "skill_type_70",
    71: "skill_type_71",
    72: "skill_type_72",
    73: "skill_type_73",
    74: "none",
    75: "skill_type_75",
    76: "skill_type_76",
    77: "skill_type_35_43_60_77",
    78: "skill_type_78",
    79: "skill_type_79",
    81: "skill_type_81",
    83: "none",
    90: "skill_type_90",
    91: "none",
    92: "skill_type_16_92",
    93: "none",
    94: "none",
    95: "skill_type_95",
    96: "none",
    97: "none",
    98: "none",
    99: "none",
    100: "skill_type_100",
    103: "none",
    105: "skill_type_105",
    106: "skill_type_106",
    107: "none",
    110: "skill_type_110",
    111: "skill_type_17",
    114: "none",
    115: "none",
    116: "skill_action_type_116",
    121: "skill_action_type_121",
    123: "skill_action_type_123",
    124: "skill_action_type_124",
    125: "skill_action_type_125",
}


class SkillActionType(Enum):
    UNKNOWN = 0  # 未知
    DAMAGE = 1  # 造成伤害
    MOVE = 2  # 位移
    CHANGE_ENEMY_POSITION = 3  # 改变对方位置
    HEAL = 4  # 回复 HP
    CURE = 5  # 回复 HP
    BARRIER = 6  # 护盾
    CHOOSE_ENEMY = 7  # 指定攻击对象
    CHANGE_ACTION_SPEED = 8  # 行动速度变更
    DOT = 9  # 持续伤害
    AURA = 10  # buff/debuff
    CHARM = 11  # 魅惑/混乱
    BLIND = 12  # 黑暗
    SILENCE = 13  # 沉默
    CHANGE_MODE = 14  # 行动模式变更
    SUMMON = 15  # 召唤
    CHANGE_TP = 16  # TP 相关
    TRIGGER = 17  # 触发条件
    CHARGE = 18  # 蓄力
    DAMAGE_CHARGE = 19  # 伤害充能
    TAUNT = 20  # 挑衅
    INVINCIBLE = 21  # 回避
    CHANGE_PATTERN = 22  # 改变循环
    IF_STATUS = 23  # 判定对象状态
    REVIVAL = 24  # 复活
    CONTINUOUS_ATTACK = 25  # 连续攻击
    ADDITIVE = 26  # 系数提升
    MULTIPLE = 27  # 倍率
    IF_SP_STATUS = 28  # 特殊条件
    NO_UB = 29  # 无法使用 UB
    KILL_ME = 30  # 立即死亡
    CONTINUOUS_ATTACK_NEARBY = 31  # 近身连续攻击
    LIFE_STEAL = 32  # HP 吸收
    STRIKE_BACK = 33  # 反伤
    ACCUMULATIVE_DAMAGE = 34  # 伤害递增
    SEAL = 35  # 特殊标记
    ATTACK_FIELD = 36  # 攻击领域展开
    HEAL_FIELD = 37  # 治疗领域展开
    AURA_FIELD = 38  # buff/debuff 领域展开
    DOT_FIELD = 39  # 持续伤害领域展开
    CHANGE_ACTION_SPEED_FIELD = 40  # 范围行动速度变更
    CHANGE_UB_TIME = 41  # 改变 UB 时间
    LOOP_TRIGGER = 42  # 触发
    IF_TARGETED = 43  # 拥有标记时触发
    WAVE_START = 44  # 每场战斗开始时
    SKILL_COUNT = 45  # 技能次数
    RATE_DAMAGE = 46  # 比例伤害
    UPPER_LIMIT_ATTACK = 47  # 攻击上限
    HOT = 48  # 持续治疗
    DISPEL = 49  # 移除增益
    CHANNEL = 50  # 持续动作
    DIVISION = 51  # 分裂
    CHANGE_WIDTH = 52  # 改变单位距离
    IF_HAS_FIELD = 53  # 特殊状态：领域存在时
    STEALTH = 54  # 潜伏
    MOVE_PART = 55  # 移动部分距离
    COUNT_BLIND = 56  # 千里眼
    COUNT_DOWN = 57  # 延迟攻击
    STOP_FIELD = 58  # 解除领域
    INHIBIT_HEAL_ACTION = 59  # 回复妨碍
    ATTACK_SEAL = 60  # 标记给予
    FEAR = 61  # 恐慌
    AWE = 62  # 畏惧
    LOOP = 63  # 循环动作
    REINDEER = 69  # 变身
    HP_CHANGE = 70  # HP 变化
    EXEMPTION_DEATH = 71  # 免死
    DAMAGE_REDUCE = 72  # 伤害减免
    LOG_BARRIER = 73  # 伤害护盾
    DIVIDE = 74  # 系数除以
    HIT_COUNT = 75  # 依据攻击次数增伤
    HEAL_DOWN = 76  # HP 回复量变化
    IF_BUFF_SEAL = 77  # 被动叠加标记
    DMG_TAKEN_UP = 78  # 被击伤害上升
    ACTION_DOT = 79  # 行动时，造成伤害
    NO_TARGET = 81  # 无效目标
    SUPERIMPOSE_CHANGE_ACTION_SPEED = 83  # 可叠加行动速度变更
    EX = 90  # EX 被动
    CHANGE_TP_RATIO = 92
    IGNORE_TAUNT = 93  # 无视挑衅
    SPECIAL_EFFECT = 94  # 技能特效
    HIDE = 95  # 隐匿
    TP_FIELD = 96  # 范围 TP 回复
    TP_HIT = 97  # 受击 tp 回复
    TP_HIT_REDUCE = 98  # 改变 TP 减少时倍率
    SPEED_FIELD = 99  # 范围加速

    EX_EQUIP = 901  # EX 装备被动
    EX_EQUIP_HALF = 902  # EX 装备被动（半）
    IGNORE_SPEED_DOWN = 100  # 免疫无法行动的异常状态
    SEAL_V2 = 101  # 特殊标记（新）
    ACCUMULATIVE_DAMAGE_V2 = 102  # 伤害递增（新）
    COPY_ATK = 103  # 复制攻击
    ENVIRONMENT = 105  # 环境效果
    GUARD = 106  # 守护
    SUM_CRITICAL = 107  # 暴击伤害合计
    DOT_UP = 110  # 持续伤害上升
    TRIGGER_V2 = 111  # 触发条件（新）
    SEAL_COUNT = 114  # 特殊标记计数
    AURA_V2 = 115  # buff/debuff（新）
    PERSISTENT = 116  # 执着状态
    MAGIC_CHANGE = 121  # 幻化状态
    MAGIC_CHANGE_REDUCE_DAMAGE = 123  # 减伤状态
    TRANSFER_DAMAGE = 124  # 护盾（转移伤害）
    CANNOT_SELECTED = 125  # 无法被选中
    BUFF_DOT = 128  # 持续伤害易伤
    DAMAGE_TO_DOT = 129  # 伤害转持续伤害
    CHANGE_DEF_MAX = 130  # 改变防御力上限


class StringResources(Enum):
    FIRE = "火"
    WATER = "水"
    WIND = "风"
    LIGHT = "光"
    DARK = "暗"
    UNKNOWN = "\?"
    NONE = ""
    SKILL_TYPE_1 = "伤害"
    SKILL_TYPE_2 = "位移"
    SKILL_TYPE_4_5 = "治疗"
    SKILL_TYPE_6 = "护盾"
    SKILL_TYPE_12 = "黑暗"
    SKILL_TYPE_13 = "沉默"
    SKILL_TYPE_14 = "模式变更"
    SKILL_TYPE_15 = "召唤"
    SKILL_TYPE_16_92 = "TP"
    SKILL_TYPE_17 = "条件"
    SKILL_TYPE_18_19 = "蓄力"
    SKILL_TYPE_20 = "挑衅"
    SKILL_TYPE_21 = "回避"
    SKILL_TYPE_22 = "循环变更"
    SKILL_TYPE_24 = "复活"
    SKILL_TYPE_30 = "即死"
    SKILL_TYPE_32 = "HP吸收"
    SKILL_TYPE_33 = "反伤"
    SKILL_TYPE_34 = "伤害递增"
    SKILL_TYPE_35_43_60_77 = "标记"
    SKILL_TYPE_36_37_38_39_40 = "领域"
    SKILL_TYPE_42 = "触发"
    SKILL_TYPE_44 = "进场"
    SKILL_TYPE_46 = "比例伤害"
    SKILL_TYPE_48 = "持续回复"
    SKILL_TYPE_49 = "移除"
    SKILL_TYPE_50 = "持续动作"
    SKILL_TYPE_54 = "潜伏"
    SKILL_TYPE_56 = "千里眼"
    SKILL_TYPE_57 = "延时"
    SKILL_TYPE_58 = "解除领域"
    SKILL_TYPE_59 = "回复妨碍"
    SKILL_TYPE_61 = "恐慌"
    SKILL_TYPE_62 = "畏惧"
    SKILL_TYPE_63 = "持续效果"
    SKILL_TYPE_69 = "变身"
    SKILL_TYPE_70 = "HP变化"
    SKILL_TYPE_71 = "免死"
    SKILL_TYPE_72 = "减伤"
    SKILL_TYPE_73 = "伤害护盾"
    SKILL_TYPE_75 = "次数触发"
    SKILL_TYPE_76 = "HP回复量"
    SKILL_TYPE_78 = "被击伤害"
    SKILL_TYPE_79 = "行动伤害"
    SKILL_TYPE_81 = "无效目标"
    SKILL_TYPE_90 = "被动"
    SKILL_TYPE_901_902 = "装备"
    SKILL_TYPE_95 = "隐匿"
    SKILL_TYPE_100 = "免疫"
    SKILL_TYPE_105 = "环境"
    SKILL_TYPE_106 = "守护"
    SKILL_TYPE_110 = "持续伤害易伤"
    SKILL_ACTION_TYPE_116 = "执着"
    SKILL_ACTION_TYPE_121 = "幻化"
    SKILL_ACTION_TYPE_123 = "减伤"
    SKILL_ACTION_TYPE_124 = "转移伤害"
    SKILL_ACTION_TYPE_125 = "无法选中"
    SKILL_ACTION_TYPE_128 = "持续伤害增强<"
    SKILL_ACTION_TYPE_129 = "伤害转化"
    SKILL_STATUS_100 = "无法行动"
    SKILL_STATUS_101 = "加速状态"
    SKILL_STATUS_200 = "失明"
    SKILL_STATUS_300 = "魅惑状态"
    SKILL_STATUS_400 = "挑衅状态"
    SKILL_STATUS_500 = "烧伤状态"
    SKILL_STATUS_501 = "诅咒状态"
    SKILL_STATUS_502 = "中毒状态"
    SKILL_STATUS_503 = "猛毒状态"
    SKILL_STATUS_504 = "咒术状态"
    SKILL_STATUS_511 = "诅咒或咒术状态"
    SKILL_STATUS_512 = "中毒或猛毒状态"
    SKILL_STATUS_710 = "BREAK 状态"
    SKILL_STATUS_900 = "HP 全满状态"
    SKILL_STATUS_1400 = "变身状态"
    SKILL_STATUS_1600 = "恐慌状态"
    SKILL_STATUS_1601 = "隐匿状态"
    SKILL_STATUS_1700_21 = "物理防御减少状态"
    SKILL_STATUS_1700_41 = "魔法防御减少状态"
    SKILL_STATUS_721 = "特殊标记状态"
    SKILL_STATUS_6107 = "龙之眼状态"
    SKILL_STATUS_1800 = "多目标状态"
    SKILL_STATUS_1900 = "护盾展开"
    SKILL_STATUS_3137 = "界雷"
    SKILL_STATUS_3162 = "妨魔塵"
    SKILL_STATUS_3175 = "绝冰"
    SKILL_STATUS_3207 = "忌火"
    SKILL_STATUS_6160 = "黏着状态"
    SKILL_STATUS_PHYSICAL_ATK = "物理攻击"
    SKILL_STATUS_MAGIC_ATK = "魔法攻击"
    SKILL_TARGET_NONE = "目标"
    SKILL_TARGET_2_8 = "随机"
    SKILL_TARGET_3 = "最近"
    SKILL_TARGET_4 = "最远"
    SKILL_TARGET_5_25 = "HP最低"
    SKILL_TARGET_6_26 = "HP最高"
    SKILL_TARGET_7 = "自身"
    SKILL_TARGET_9 = "最后方"
    SKILL_TARGET_10 = "最前方"
    SKILL_TARGET_11 = "范围内"
    SKILL_TARGET_12_27_37 = "TP最高"
    SKILL_TARGET_13_19_28 = "TP最低"
    SKILL_TARGET_14_29 = "物理攻击力最高"
    SKILL_TARGET_15_30 = "物理攻击力最低"
    SKILL_TARGET_16_31 = "魔法攻击力最高"
    SKILL_TARGET_17_32 = "魔法攻击力最低"
    SKILL_TARGET_18 = "召唤物"
    SKILL_TARGET_20 = "物理"
    SKILL_TARGET_21 = "魔法"
    SKILL_TARGET_22 = "随机召唤物"
    SKILL_TARGET_23 = "自身召唤物"
    SKILL_TARGET_24 = "领主"
    SKILL_TARGET_33 = "暗影"
    SKILL_TARGET_34 = "除自身以外"
    SKILL_TARGET_35 = "剩余HP最高"
    SKILL_TARGET_36 = "剩余HP最低"
    SKILL_TARGET_38 = "攻击力最高"
    SKILL_TARGET_39 = "攻击力最低"
    SKILL_TARGET_42 = "多目标"
    SKILL_TARGET_43 = "物理攻击力最高(自身除外)"
    SKILL_TARGET_44 = "剩余HP最低(自身除外)"
    SKILL_TARGET_45 = "物理防御力最低"
    SKILL_TARGET_46 = "魔法防御力最低"
    SKILL_TARGET_50 = "魔法攻击力最高(自身除外)"
    SKILL_TARGET_13XXX = "被标记"
    SKILL_TARGET_FIRE = "火天赋"
    SKILL_TARGET_WATER = "水天赋"
    SKILL_TARGET_WIND = "风天赋"
    SKILL_TARGET_LIGHT = "光天赋"
    SKILL_TARGET_DARK = "暗天赋"
    SKILL_TARGET_ASSIGNMENT_0 = "自身"
    SKILL_TARGET_ASSIGNMENT_1 = "敌人"
    SKILL_TARGET_ASSIGNMENT_2 = "己方"
    SKILL_TARGET_ASSIGNMENT_3 = "敌人和己方"
    SKILL_SHIELD_NO_EFFECT = "无效"
    SKILL_SHIELD_DEFENSE = "吸收"
    SKILL_SHIELD = "{}{}伤害的护盾"
    SKILL_ACTION = "动作"
    SKILL_ACTION_D = "动作({})"
    SKILL_EFFECT_TIME = "，持续 {} 秒"
    SKILL_ALL = "所有"
    SKILL_LEVEL_TEXT = "技能等级"
    SKILL_ATK_TEXT = "攻击力"
    SKILL_SPEED = "速度"
    SKILL_HP_MAX = "HP最大值"
    SKILL_INCREASE = "提升"
    SKILL_REDUCE = "减少"
    SKILL_FIXED = "(固定数值，无法被其他技能效果改变)"
    SKILL_PHYSICAL_CRITICAL_DAMAGE = "物理暴击伤害"
    SKILL_MAGIC_CRITICAL_DAMAGE = "魔法暴击伤害"
    SKILL_CRITICAL_DAMAGE_TAKE = "受到的暴击伤害"
    SKILL_PHYSICAL_DAMAGE_TAKE = "受到的物理伤害"
    SKILL_MAGIC_DAMAGE_TAKE = "受到的魔法伤害"
    SKILL_PHYSICAL_DAMAGE = "造成的物理伤害"
    SKILL_MAGIC_DAMAGE = "造成的魔法伤害"
    SKILL_DEPEND_ACTION = "受到动作({})影响的"
    SKILL_RANGE = "范围{}内"
    SKILL_TARGET_SINGLE = "单体"
    SKILL_TARGET_COUNT = "{}名"
    SKILL_TARGET_ALL = "全体"
    SKILL_TARGET_ORDER_NUM = "第{}近"
    SKILL_TARGET_ORDER_1 = "最近"
    SKILL_PHYSICAL = "物理"
    SKILL_PHYSICAL_STR = "物理攻击力"
    SKILL_PHYSICAL_DEF = "物理防御力"
    SKILL_MAGIC = "魔法"
    SKILL_MAGIC_STR = "魔法攻击力"
    SKILL_MAGIC_DEF = "魔法防御力"
    SKILL_MUST_HIT_PHYSICAL = "必定命中的物理"
    SKILL_MUST_HIT_MAGIC = "必定命中的魔法"
    SKILL_SUM_ATK_PHYSICAL = "(物理、魔法攻击力合计)物理"
    SKILL_SUM_ATK_MAGIC = "(物理、魔法攻击力合计)魔法"
    SKILL_ADAPTIVE_LOWER_DEFENSE = "(适应物理/魔法防御中较低的防御)"
    SKILL_CRITICAL_DAMAGE_MULTIPLE = "；暴击时，造成 {}{} 倍伤害"
    SKILL_MUST_CRITICAL = "；必定暴击"
    SKILL_IGNORE_DEF = "；无视目标{}{}防御力 "
    SKILL_ACTION_TYPE_DESC_1 = "对{}造成 {} 的{}伤害{}{}{}{}"
    SKILL_FORWARD = "向前"
    SKILL_BACKWARD = "向后"
    SKILL_AHEAD = "前方"
    SKILL_REAR = "后方"
    SKILL_MOVE = "移动至{}{} [{}]"
    SKILL_RETURN = "，动作结束后回到原来位置"
    SKILL_MOVE_SPEED = "，移动速度 [{}]"
    SKILL_HIT_UP = "击飞"
    SKILL_ACTION_TYPE_DESC_3_UP = "{}{}，高度 [{}]"
    SKILL_PUSH = "击退"
    SKILL_PULL = "拉近"
    SKILL_ACTION_TYPE_DESC_3_MOVE = "{}{}，距离 [{}]"
    SKILL_ACTION_TYPE_DESC_3_PULL = "将{}{}身前 [{}]"
    SKILL_ACTION_TYPE_DESC_4 = "使{}HP回复 {}"
    SKILL_ACTION_TYPE_DESC_6 = "对{}展开{} {}{}"
    SKILL_ACTION_TYPE_DESC_7 = "锁定{}"
    SKILL_ACTION_SPEED_CHANGE = "速度额外{}初始值的 {} 倍"
    SKILL_ACTION_SPEED_MULTIPLE = "速度变更为初始值的 {} 倍"
    SKILL_ACTION_TYPE_DESC_8 = "使{}进入 [{}] 状态{}{}"
    SKILL_ACTION_HIT_REMOVE = "，本效果将会在受到伤害时解除"
    SKILL_ACTION_DOT_INCREASE = "，伤害每秒增加基础数值的 [{}%]"
    SKILL_ACTION_TYPE_DESC_9 = "使{}进入{}状态，每秒造成伤害 {}{}{}"
    SKILL_BUFF = "增益"
    SKILL_DEBUFF = "减益"
    SKILL_BARRIER = "护盾"
    SKILL_DAMAGE = "伤害"
    SKILL_STATUS_DOWN = "状态下降"
    SKILL_STATUS_UB = "己方使用连结爆发技能"
    SKILL_ACTION_TYPE_DESC_10_BREAK = "BREAK 期间，{}{}"
    SKILL_CHARM_0 = "魅惑"
    SKILL_CHARM_1 = "混乱"
    SKILL_ACTION_TYPE_DESC_12_13 = "以 {} 的概率使{}进入{}状态{}"
    SKILL_ACTION_ATK_MISS = "；对象进行物理攻击时有 [{}%] 的概率被回避"
    SKILL_ACTION_LOOP_CHANGE = "技能循环改变{}"
    SKILL_ACTION_TYPE_DESC_14_2 = "技能循环改变，每秒降低 [{}] TP"
    SKILL_ACTION_TYPE_DESC_14_3 = "效果结束后，切换回原技能循环"
    SKILL_ACTION_TYPE_DESC_15 = "在{}{} [{}] 的位置{}"
    SKILL_ACTION_SUMMON_TARGET = "在{}{}"
    SKILL_ACTION_SUMMON_UNIT = "，召唤友方单位"
    SKILL_ACTION_TP_RECOVERY = "TP回复"
    SKILL_ACTION_TP_REDUCE = "TP减少"
    SKILL_ACTION_CONDITION = "条件：{}"
    SKILL_ACTION_TYPE_DESC_17_2 = "受到伤害时 [{}%] 概率"
    SKILL_ACTION_TYPE_DESC_17_3 = "HP [{}%] 以下"
    SKILL_ACTION_TYPE_DESC_17_4 = "死亡时 [{}%] 概率"
    SKILL_ACTION_TYPE_DESC_17_5 = "暴击时 [{}%] 概率"
    SKILL_ACTION_TYPE_DESC_17_7 = "战斗剩余时间 [{}] 秒以下"
    SKILL_ACTION_TYPE_DESC_17_8 = "隐身时 [{}%] 概率"
    SKILL_ACTION_TYPE_DESC_17_9 = "BREAK 时 [{}%] 的概率{}"
    SKILL_ACTION_TYPE_DESC_17_10 = "受到持续伤害时 [{}%] 概率"
    SKILL_ACTION_TYPE_DESC_17_11 = "所有部位 BREAK"
    SKILL_ACTION_TYPE_DESC_17_13 = "HP减少 [{}] 时"
    SKILL_ACTION_TYPE_DESC_17_17 = "被击时 [{}%] 概率触发"
    SKILL_ACTION_TYPE_DESC_18_19 = "蓄力 [{}] 秒"
    SKILL_ACTION_TYPE_DESC_18_19_DETAIL = "，动作({})效果增加 {} * 蓄力中受到的伤害"
    SKILL_ACTION_TYPE_DESC_20 = "使{}进入{}状态{}"
    SKILL_ACTION_TYPE_DESC_21_1 = "无敌"
    SKILL_ACTION_TYPE_DESC_21_2 = "回避物理攻击"
    SKILL_ACTION_TYPE_DESC_21_3 = "回避所有攻击"
    SKILL_ACTION_TYPE_DESC_21_6 = "回避 BREAK"
    SKILL_ACTION_TYPE_DESC_21_8 = "回避魔法攻击"
    SKILL_ACTION_SKILL_ANIM_CHANGE = "技能动画改变{}"
    SKILL_ACTION_IF_STATUS = "当{}在 [{}] 时，使用动作({})"
    SKILL_ACTION_IF_STATUS_NOT = "当{}不在 [{}] 时，使用动作({})"
    SKILL_ACTION_IF_MARK = "{}持有标记时，使用动作({})"
    SKILL_ACTION_IF_MARK_NOT = "{}未持有标记时，使用动作({})"
    SKILL_ACTION_IF_MARK_COUNT = "{}持有标记数量为 [{}] 时，使用动作({})"
    SKILL_ACTION_IF_MARK_COUNT_NOT = "{}持有标记数量不为 [{}] 时，使用动作({})"
    SKILL_ACTION_IF_ALONE = "{}仅剩一名时，使用动作({})"
    SKILL_ACTION_IF_ALONE_NOT = "{}多于一名时，使用动作({})"
    SKILL_ACTION_IF_HP_BELOW = "{}的HP在 [{}%] 以下时，使用动作({})"
    SKILL_ACTION_IF_HP_ABOVE = "{}的HP在 [{}%] 以上时，使用动作({})"
    SKILL_ACTION_IF_UNIT_ATK_TYPE = "{}是 [{}] 对象时，使用动作({})"
    SKILL_ACTION_RANDOM_1 = "随机：[{}%] 的概率使用动作({})，否则使用动作({})"
    SKILL_ACTION_RANDOM_2 = "随机：[{}%] 的概率使用动作({})"
    SKILL_ACTION_TYPE_DESC_24 = "复活{}，并回复其 [{}%] HP"
    SKILL_ACTION_TYPE_DESC_ADDITIVE = "增加"
    SKILL_ACTION_TYPE_DESC_SUBTRACT = "减少"
    SKILL_ACTION_TYPE_DESC_MULTIPLE = "乘以"
    SKILL_ACTION_TYPE_DESC_DIVIDE = "除以"
    SKILL_ACTION_CHANGE_COE = "动作({})的数值{{{}}}{} {}"
    SKILL_ACTION_LIMIT = "；叠加上限 {}"
    SKILL_ACTION_LIMIT_INT = "；叠加上限 [{}]"
    SKILL_ACTION_DAMAGE_LIMIT_INT = "；伤害上限 [{}]"
    SKILL_ACTION_CHANGE_COE_0 = "{} * [剩余的HP]"
    SKILL_ACTION_CHANGE_COE_1 = "{} * [损失的HP]"
    SKILL_ACTION_CHANGE_COE_2 = "{} * [击杀数量]"
    SKILL_ACTION_CHANGE_COE_4 = "{} * [{}数量]"
    SKILL_ACTION_CHANGE_COE_5 = "{} * [受到伤害的目标数量]"
    SKILL_ACTION_CHANGE_COE_6 = "{} * [造成的伤害]"
    SKILL_ACTION_CHANGE_COE_7_10 = "{} * [{}的{}]"
    SKILL_ACTION_CHANGE_COE_12 = "{} * [后方{}数量]"
    SKILL_ACTION_CHANGE_COE_13 = "{} * [损失的HP比例]"
    SKILL_ACTION_CHANGE_COE_15 = "{} * [{}剩余HP]"
    SKILL_ACTION_CHANGE_COE_16 = "{} * [{}消耗的TP]"
    SKILL_ACTION_CHANGE_COE_102 = "{} * [小眼球数量]"
    SKILL_ACTION_CHANGE_COE_SKILL_COUNT = "{} * [技能计数]"
    SKILL_ACTION_CHANGE_COE_MARK_COUNT = "{} * [标记层数]"
    SKILL_ACTION_CHANGE_TO_FLIGHT_STATUS = "，进入[飞行]状态"
    SKILL_ACTION_CHANGE_MODE = "行动模式改变{}{}"
    SKILL_ACTION_SP_IF_RATE = "以 [{}%] 的概率使用动作({})"
    SKILL_ACTION_SP_IF_DOT = "{}身上有持续伤害时，使用动作({})"
    SKILL_ACTION_SP_IF_DOT_NOT = "{}身上没有持续伤害时，使用动作({})"
    SKILL_ACTION_SP_IF_SKILL_COUNT = "{}的技能计数 ≥ [{}] 时，使用动作({})"
    SKILL_ACTION_SP_IF_SKILL_COUNT_NOT = "{}的技能计数 ﹤ [{}] 时，使用动作({})"
    SKILL_ACTION_SP_IF_MARK_COUNT = "{}的标记层数 ≥ [{}] 时，使用动作({})"
    SKILL_ACTION_SP_IF_MARK_COUNT_NOT = "{}的标记层数 ﹤ [{}] 时，使用动作({})"
    SKILL_ACTION_SP_IF_UNIT_COUNT = (
        "隐身状态的单位除外，{}的数量是 [{}] 时，使用动作({})"
    )
    SKILL_ACTION_SP_IF_UNIT_COUNT_NOT = (
        "隐身状态的单位除外，{}的数量不是 [{}] 时，使用动作({})"
    )
    SKILL_ACTION_SP_IF_UNIT_EXIST = "{}中存在单位时，使用动作({})"
    SKILL_ACTION_SP_IF_UNIT_EXIST_NOT = "{}中不存在单位时，使用动作({})"
    SKILL_ACTION_SP_IF_KILL = "上一个动作击杀了单位时，使用动作({})"
    SKILL_ACTION_SP_IF_KILL_NOT = "上一个动作未击杀单位时，使用动作({})"
    SKILL_ACTION_SP_IF_CRITICAL = "技能暴击时，使用动作({})"
    SKILL_ACTION_SP_IF_CRITICAL_NOT = "技能未暴击时，使用动作({})"
    SKILL_ACTION_TYPE_DESC_29 = "无 UB 技能"
    SKILL_ACTION_TYPE_DESC_30 = "{}死亡"
    SKILL_ACTION_TYPE_DESC_32 = "为{}的下 [{}] 次攻击附加{} {} 的效果"
    SKILL_ACTION_TYPE_DESC_33 = "{}，受到{}伤害时反弹 {} 伤害{}，生效 [{}] 次"
    SKILL_ACTION_TYPE_DESC_33_HP = "，并回复HP"
    SKILL_ACTION_TYPE_DESC_34 = "每次攻击当前的目标，将会追加伤害 {}{}"
    SKILL_ACTION_TYPE_DESC_35 = "对{}追加 [{}] 层标记{}{}"
    SKILL_ACTION_TYPE_DESC_35_REDUCE = "{}减少 [{}] 层标记"
    SKILL_ACTION_TYPE_DESC_36_DAMAGE = "每秒造成 {} {}伤害"
    SKILL_ACTION_TYPE_DESC_FIELD = "展开{1}的领域，范围 [{0}]{2}"
    SKILL_ACTION_TYPE_DESC_37_HEAL = "每秒回复 {} HP"
    SKILL_ACTION_TYPE_DESC_38_ACTION = "，持续施放动作({})"
    SKILL_ACTION_TYPE_DESC_42_2 = "[{}] 秒内受到伤害时，以 {} 的概率使用动作({})"
    SKILL_ACTION_TYPE_DESC_42_14 = (
        "[{}] 秒内受到无法行动、击飞、拉近伤害时，以 {} 的概率使用{}"
    )
    SKILL_ACTION_TYPE_DESC_44 = "战斗开始 [{}] 秒后入场"
    SKILL_ACTION_TYPE_DESC_45 = "技能计数加 [1] {}"
    SKILL_ACTION_TYPE_DESC_46_1 = "对{}造成最大HP {} 伤害"
    SKILL_ACTION_TYPE_DESC_46_2 = "对{}造成剩余HP {} 伤害"
    SKILL_ACTION_TYPE_DESC_46_3 = "对{}造成初始最大HP {} 伤害"
    SKILL_ACTION_TYPE_DESC_47 = "对低等级的玩家造成的伤害将被减轻"
    SKILL_ACTION_TYPE_DESC_48 = "每秒回复{}的 {} {}{}"
    SKILL_ACTION_TYPE_DESC_49 = "{} 概率移除{}的{}"
    SKILL_ACTION_TYPE_DESC_50 = "{}{}{}，受到 [{}] 次伤害时中断"
    SKILL_ACTION_TYPE_DESC_52 = "将模型的宽度变为 [{}]"
    SKILL_ACTION_TYPE_DESC_53 = "特定的领域效果存在时使用动作({}){}"
    SKILL_ACTION_TYPE_DESC_53_2 = "，否则使用动作({})"
    SKILL_ACTION_TYPE_DESC_54 = "进入隐身状态{}"
    SKILL_ACTION_TYPE_DESC_55 = "使部位{}向前移动 [{}] ，随后使其返回原位置"
    SKILL_ACTION_TYPE_DESC_56_1 = "使{}的物理攻击必定被回避{}"
    SKILL_ACTION_TYPE_DESC_56_2 = "使{}的下 {} 次物理攻击必定被回避"
    SKILL_ACTION_TYPE_DESC_57 = "对{}设置倒计时，[{}] 秒后触发动作({})"
    SKILL_ACTION_TYPE_DESC_58 = "解除第{}个技能的动作({})展开的领域"
    SKILL_ACTION_TYPE_DESC_59 = "{}，HP回复效果减少 [{}%] {}"
    SKILL_ACTION_TYPE_DESC_60_0 = "，追加 [1] 层标记{}{}"
    SKILL_ACTION_TYPE_DESC_60_1 = "自身每次攻击{}时{}"
    SKILL_ACTION_TYPE_DESC_60_2 = "{}每次造成伤害时{}"
    SKILL_ACTION_TYPE_DESC_60_3 = "{}每次造成暴击时{}"
    SKILL_ACTION_TYPE_DESC_60_4 = "{}每次攻击命中敌人时{}"
    SKILL_ACTION_TYPE_DESC_61 = "以 {} 的概率使{}进入{}状态{}"
    SKILL_ACTION_TYPE_DESC_62_0 = (
        "{}的UB对任意目标造成伤害或直接回复时，使其效果值降低 {}{}"
    )
    SKILL_ACTION_TYPE_DESC_62_1 = (
        "{}的UB或技能对任意目标造成伤害或直接回复时，使其效果值降低 {}{}"
    )
    SKILL_ACTION_TYPE_DESC_63_SUCCESS = "持续时间结束后，使用动作({})；"
    SKILL_ACTION_TYPE_DESC_63_FAILURE = "效果被中断后，使用动作({})；"
    SKILL_ACTION_TYPE_DESC_63 = "每 {} 秒使用 1 次动作({})，最长持续 [{}] 秒；受到的伤害量超过 [{}] 时中断此效果；"
    SKILL_ACTION_TYPE_DESC_69 = "使{}变身{}"
    SKILL_ACTION_TYPE_DESC_71 = "赋予{}「受到致死伤害时，回复 {} HP」的效果{}"
    SKILL_ACTION_TYPE_DESC_72 = "赋予{}承受{}伤害减少{}的效果{}"
    SKILL_ACTION_TYPE_DESC_73 = (
        "为{}展开护盾，在单个动作中受到的伤害超过 [{}] 时，伤害值将衰减{}"
    )
    SKILL_ACTION_TYPE_DESC_75 = "每造成 [{}] 次伤害时，触发动作({}) {}"
    SKILL_ACTION_TYPE_DESC_76 = "{}治疗量变为原来的 {}{}"
    SKILL_ACTION_TYPE_DESC_77 = "每当{} [{}] 时，为自身追加 [{}] 层标记{}{}"
    SKILL_ACTION_TYPE_DESC_77_1 = "受到"
    SKILL_ACTION_TYPE_DESC_78 = "使{}受到的伤害额外{} {} 倍{}{}"
    SKILL_ACTION_TYPE_DESC_78_1 = "减益和异常状态数量"
    SKILL_ACTION_TYPE_DESC_79 = "{}行动时，受到{} {} 伤害{}{}"
    SKILL_ACTION_TYPE_DESC_81 = "{}变更为无法被攻击的目标"
    SKILL_ACTION_TYPE_DESC_90 = "{}{}提升 {}"
    SKILL_ACTION_TYPE_DESC_901 = "战斗开始时生效"
    SKILL_ACTION_TYPE_DESC_902 = "战斗时间剩余{}秒时生效"
    SKILL_ACTION_TYPE_DESC_92 = "使{}受击获得的TP变更为初始值的 [{}] 倍"
    SKILL_ACTION_TYPE_DESC_93 = "攻击{}时，无视挑衅效果"
    SKILL_ACTION_TYPE_DESC_94 = "{}附加技能特效"
    SKILL_ACTION_TYPE_DESC_95 = "{}进入隐匿状态{}"
    SKILL_ACTION_TYPE_DESC_96_TP = "每秒回复 {} TP"
    SKILL_ACTION_TYPE_DESC_97 = "；受击时减少 [1] 层标记，TP回复 [{}]"
    SKILL_ACTION_TYPE_DESC_98 = "使{}受到TP降低时，效果变更为初始值的 [{}] 倍{}"
    SKILL_ACTION_TYPE_DESC_100 = "{}免疫 [无法行动] 异常状态{}{}"
    SKILL_ACTION_TYPE_DESC_100_COUNT = " [{}] 次"
    SKILL_ACTION_TYPE_DESC_101 = "{}攻击时，对敌人追加 [{}] 层标记{}{}"
    SKILL_ACTION_TYPE_DESC_101_REDUCE = "{}攻击时，敌人减少 [{}] 层标记"
    SKILL_ACTION_TYPE_DESC_103 = "动作({})造成的伤害将依据{}的攻击力"
    SKILL_ACTION_TYPE_UNKNOWN = "{}目标：{}；类型：{}；数值：{}{}"
    SKILL_ACTION_TYPE_DESC_105 = "发动 [{}] 环境效果{}"
    SKILL_ACTION_TYPE_DESC_106 = "赋予{} [{}] 状态，并代替其承受伤害{}"
    SKILL_ACTION_TYPE_DESC_106_TYPE_COMMON = "守护"
    SKILL_ACTION_TYPE_DESC_106_TYPE_141 = "堕天使的守护"
    SKILL_ACTION_TYPE_DESC_107 = "动作({})暴击率依据物理暴击与魔法暴击之和"
    SKILL_ACTION_TYPE_DESC_110 = "使{}受到持续伤害时，额外承受 {} 的伤害{}"
    SKILL_ACTION_TYPE_DESC_111 = "当{}{}时，使用动作({})"
    SKILL_ACTION_TYPE_DESC_111_1 = "当{}标记数量 {} [{}] 时，使用动作({})"
    SKILL_ACTION_TYPE_DESC_111_2 = "受到暴击伤害"
    SKILL_ACTION_TYPE_DESC_114 = "对{}追加 [{}] 层标记，{}，受到伤害时，减少 [1] 层标记，并使用动作({})和动作({}){}"
    SKILL_ACTION_TYPE_DESC_114_AURA = "己方受到的伤害降低 [{}%]"
    SKILL_ACTION_TYPE_DESC_116_121_123_124 = "使{}进入 [{}] 状态{}"
    SKILL_ACTION_TYPE_DESC_123_1 = "受到的伤害减少{}"
    SKILL_ACTION_TYPE_DESC_125 = "使{}进入 [{}] 状态（持有标记时，不会成为攻击目标）"
    SKILL_ACTION_TYPE_DESC_128 = "使{}受到的持续伤害的间隔和时间延长 [{}] 倍{}"
    SKILL_ACTION_TYPE_DESC_129 = (
        "使{}受到的 {} 伤害转化为持续伤害{}；该持续伤害不回复 TP"
    )
    SKILL_ACTION_TYPE_DESC_130 = "使{}受到伤害时，按物理/魔法防御中较高的防御计算伤害"
    SKILL_AILMENT_1 = "减速"
    SKILL_AILMENT_2 = "加速"
    SKILL_AILMENT_3 = "麻痹"
    SKILL_AILMENT_4 = "冻结"
    SKILL_AILMENT_5 = "束缚"
    SKILL_AILMENT_6 = "睡眠"
    SKILL_AILMENT_7_12_14 = "眩晕"
    SKILL_AILMENT_8 = "石化"
    SKILL_AILMENT_9 = "拘留"
    SKILL_AILMENT_10 = "昏迷"
    SKILL_AILMENT_11 = "时间停止"
    SKILL_AILMENT_13 = "结晶"
    SKILL_AILMENT_EXTRA = "(额外)"
    SKILL_AILMENT_FIELD = "(范围)"
    SKILL_DOT_0 = "拘留(造成伤害)"
    SKILL_DOT_1_7 = "中毒"
    SKILL_DOT_2 = "烧伤"
    SKILL_DOT_3_8 = "诅咒"
    SKILL_DOT_4 = "猛毒"
    SKILL_DOT_5 = "咒术"
    SKILL_DOT_11 = "绝怠灵度"
    ATTR_HP = "HP"
    ATTR_LIFE_STEAL = "HP吸收"
    ATTR_ATK = "物理攻击力"
    ATTR_MAGIC_STR = "魔法攻击力"
    ATTR_DEF = "物理防御力"
    ATTR_MAGIC_DEF = "魔法防御力"
    ATTR_PHYSICAL_CRITICAL = "物理暴击"
    ATTR_MAGIC_CRITICAL = "魔法暴击"
    ATTR_PHYSICAL_PENETRATE = "物理穿透"
    ATTR_MAGIC_PENETRATE = "魔法穿透"
    ATTR_ACCURACY = "命中"
    ATTR_DODGE = "回避"
    ATTR_WAVE_HP_RECOVERY = "HP回复"
    ATTR_HP_RECOVERY_RATE = "回复上升"
    ATTR_WAVE_ENERGY_RECOVERY = "TP回复"
    ATTR_ENERGY_RECOVERY_RATE = "TP上升"
    ATTR_ENERGY_REDUCE_RATE = "TP减少"
    ATTR_TP = "TP"
    DAY = "{}天"
    HOUR = "{}时"
    MINUTE = "{}分"
    MAGIC = "魔法"
    PHYSICAL = "物理"

    @staticmethod
    def get(resource_key: str, *args):
        """获取字符串并格式化"""
        return StringResources[resource_key.upper()].value.format(*args)


STORY_STATE_DICT = {
    1: "HP",
    2: "物理攻击",
    3: "物理防御",
    4: "魔法攻击",
    5: "魔法防御",
    6: "物理暴击",
    7: "魔法暴击",
    8: "闪避",
    9: "生命偷取",
    10: "HP回复",
    11: "TP回复",
    14: "TP上升",
    15: "回复上升",
    17: "命中",
}


class Color(Enum):
    gold = "#dfb340"
    red = "#a5366f"
    green = "#7aa57b"
    orange = "#ed6c51"
    primary = "#a5366f"
    black = "#000000"
    white = "#ffffff"
    purple = "#b476cd"
    pink = "#f8b1d7"


class CalendarEventType(Enum):
    UNKNOWN = 404
    TOWER = 1
    SP_DUNGEON = -1
    TDF = -2
    COLOSSEUM = -3
    DAILY = 18
    LOGIN = 19
    FORTUNE = 20
    N_DROP = 31
    N_MANA = 41
    H_DROP = 32
    H_MANA = 42
    VH_DROP = 39
    VH_MANA = 49
    EXPLORE = 34
    SHRINE = 37
    TEMPLE = 38
    DUNGEON = 45

    @classmethod
    def get_by_value(cls, value: int) -> "CalendarEventType":
        return next((item for item in cls if item.value == value), cls.UNKNOWN)
