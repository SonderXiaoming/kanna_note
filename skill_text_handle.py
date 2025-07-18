from math import e
import re
from typing import List

from .table import EnemyParameter, SkillData, UnitSkillData
from .model import ShowCoe, SkillActionData, SkillActionText
from .base import SKILL_DESCRIPTIONS, SkillActionType, StringResources


def get_skill_level(skill_data: UnitSkillData, parameter: EnemyParameter) -> dict:
    skill_dict = {}
    if skill_data.union_burst:
        skill_dict[skill_data.union_burst] = parameter.union_burst_level
    if skill_data.union_burst_evolution:
        skill_dict[skill_data.union_burst_evolution] = parameter.union_burst_level
    if skill_data.main_skill_1:
        skill_dict[skill_data.main_skill_1] = parameter.main_skill_lv_1
    if skill_data.main_skill_evolution_1 and (
        skill_data.sp_skill_1 != 1064101 or skill_data.main_skill_evolution_1 != 1065012
    ):
        skill_dict[skill_data.main_skill_evolution_1] = parameter.main_skill_lv_1
    if skill_data.main_skill_2:
        skill_dict[skill_data.main_skill_2] = parameter.main_skill_lv_2
    if skill_data.main_skill_evolution_2:
        skill_dict[skill_data.main_skill_evolution_2] = parameter.main_skill_lv_2
    if skill_data.main_skill_3:
        skill_dict[skill_data.main_skill_3] = parameter.main_skill_lv_3
    if skill_data.main_skill_4:
        skill_dict[skill_data.main_skill_4] = parameter.main_skill_lv_4
    if skill_data.main_skill_5:
        skill_dict[skill_data.main_skill_5] = parameter.main_skill_lv_5
    if skill_data.main_skill_6:
        skill_dict[skill_data.main_skill_6] = parameter.main_skill_lv_6
    if skill_data.main_skill_7:
        skill_dict[skill_data.main_skill_7] = parameter.main_skill_lv_7
    if skill_data.main_skill_8:
        skill_dict[skill_data.main_skill_8] = parameter.main_skill_lv_8
    if skill_data.main_skill_9:
        skill_dict[skill_data.main_skill_9] = parameter.main_skill_lv_9
    if skill_data.main_skill_10:
        skill_dict[skill_data.main_skill_10] = parameter.main_skill_lv_10
    if skill_data.ex_skill_1:
        skill_dict[skill_data.ex_skill_1] = parameter.ex_skill_lv_1
    if skill_data.ex_skill_evolution_1:
        skill_dict[skill_data.ex_skill_evolution_1] = parameter.ex_skill_lv_1
    if skill_data.ex_skill_2:
        skill_dict[skill_data.ex_skill_2] = parameter.ex_skill_lv_2
    if skill_data.ex_skill_evolution_2:
        skill_dict[skill_data.ex_skill_evolution_2] = parameter.ex_skill_lv_2
    if skill_data.ex_skill_3:
        skill_dict[skill_data.ex_skill_3] = parameter.ex_skill_lv_3
    if skill_data.ex_skill_evolution_3:
        skill_dict[skill_data.ex_skill_evolution_3] = parameter.ex_skill_lv_3
    if skill_data.ex_skill_4:
        skill_dict[skill_data.ex_skill_4] = parameter.ex_skill_lv_4
    if skill_data.ex_skill_evolution_4:
        skill_dict[skill_data.ex_skill_evolution_4] = parameter.ex_skill_lv_4
    if skill_data.ex_skill_5:
        skill_dict[skill_data.ex_skill_5] = parameter.ex_skill_lv_5
    if skill_data.ex_skill_evolution_5:
        skill_dict[skill_data.ex_skill_evolution_5] = parameter.ex_skill_lv_5
    return skill_dict


def get_skill_ids(skill: UnitSkillData):
    skill_dict = {
        "normal": [],
        "sp": [],
    }

    skill_type_dict = {}
    if skill.union_burst:
        skill_dict["normal"].append(skill.union_burst)
        skill_type_dict[skill.union_burst] = "连结爆发"
    if skill.union_burst_evolution:
        skill_dict["normal"].append(skill.union_burst_evolution)
        skill_type_dict[skill.union_burst_evolution] = "连结爆发+"
    if skill.main_skill_1:
        skill_dict["normal"].append(skill.main_skill_1)
        skill_type_dict[skill.main_skill_1] = "技能1"
    if skill.main_skill_evolution_1 and (
        skill.sp_skill_1 != 1064101 or skill.main_skill_evolution_1 != 1065012
    ):  # 日服雪菲
        skill_dict["normal"].append(skill.main_skill_evolution_1)
        skill_type_dict[skill.main_skill_evolution_1] = "技能1+"

    if skill.main_skill_2:
        skill_dict["normal"].append(skill.main_skill_2)
        skill_type_dict[skill.main_skill_2] = "技能2"
    if skill.main_skill_evolution_2:
        skill_dict["normal"].append(skill.main_skill_evolution_2)
        skill_type_dict[skill.main_skill_evolution_2] = "技能2+"
    if skill.main_skill_3:
        skill_dict["normal"].append(skill.main_skill_3)
        skill_type_dict[skill.main_skill_3] = "技能3"
    if skill.main_skill_4:
        skill_dict["normal"].append(skill.main_skill_4)
        skill_type_dict[skill.main_skill_4] = "技能4"
    if skill.main_skill_5:
        skill_dict["normal"].append(skill.main_skill_5)
        skill_type_dict[skill.main_skill_5] = "技能5"
    if skill.main_skill_6:
        skill_dict["normal"].append(skill.main_skill_6)
        skill_type_dict[skill.main_skill_6] = "技能6"
    if skill.main_skill_7:
        skill_dict["normal"].append(skill.main_skill_7)
        skill_type_dict[skill.main_skill_7] = "技能7"
    if skill.main_skill_8:
        skill_dict["normal"].append(skill.main_skill_8)
        skill_type_dict[skill.main_skill_8] = "技能8"
    if skill.main_skill_9:
        skill_dict["normal"].append(skill.main_skill_9)
        skill_type_dict[skill.main_skill_9] = "技能9"
    if skill.main_skill_10:
        skill_dict["normal"].append(skill.main_skill_10)
        skill_type_dict[skill.main_skill_10] = "技能10"

    if skill.ex_skill_1:
        skill_dict["normal"].append(skill.ex_skill_1)
        skill_type_dict[skill.ex_skill_1] = "额外技能"
    if skill.ex_skill_evolution_1:
        skill_dict["normal"].append(skill.ex_skill_evolution_1)
        skill_type_dict[skill.ex_skill_evolution_1] = "额外技能+"
    if skill.ex_skill_2:
        skill_dict["normal"].append(skill.ex_skill_2)
        skill_type_dict[skill.ex_skill_2] = "额外技能2"
    if skill.ex_skill_evolution_2:
        skill_dict["normal"].append(skill.ex_skill_evolution_2)
        skill_type_dict[skill.ex_skill_evolution_2] = "额外技能2+"
    if skill.ex_skill_3:
        skill_dict["normal"].append(skill.ex_skill_3)
        skill_type_dict[skill.ex_skill_3] = "额外技能3"
    if skill.ex_skill_evolution_3:
        skill_dict["normal"].append(skill.ex_skill_evolution_3)
        skill_type_dict[skill.ex_skill_evolution_3] = "额外技能3+"
    if skill.ex_skill_4:
        skill_dict["normal"].append(skill.ex_skill_4)
        skill_type_dict[skill.ex_skill_4] = "额外技能4"
    if skill.ex_skill_evolution_4:
        skill_dict["normal"].append(skill.ex_skill_evolution_4)
        skill_type_dict[skill.ex_skill_evolution_4] = "额外技能4+"
    if skill.ex_skill_5:
        skill_dict["normal"].append(skill.ex_skill_5)
        skill_type_dict[skill.ex_skill_5] = "额外技能5"
    if skill.ex_skill_evolution_5:
        skill_dict["normal"].append(skill.ex_skill_evolution_5)
        skill_type_dict[skill.ex_skill_evolution_5] = "额外技能5+"
    if skill.sp_union_burst:
        skill_dict["sp"].append(skill.sp_union_burst)
        skill_type_dict[skill.sp_union_burst] = "SP连结爆发"
    if skill.sp_skill_1:
        skill_dict["sp"].append(skill.sp_skill_1)
        skill_type_dict[skill.sp_skill_1] = "SP技能1"
    if skill.sp_skill_evolution_1:
        skill_dict["sp"].append(skill.sp_skill_evolution_1)
        skill_type_dict[skill.sp_skill_evolution_1] = "SP技能1+"
    if skill.sp_skill_2:
        skill_dict["sp"].append(skill.sp_skill_2)
        skill_type_dict[skill.sp_skill_2] = "SP技能2"
    if skill.sp_skill_evolution_2:
        skill_dict["sp"].append(skill.sp_skill_evolution_2)
        skill_type_dict[skill.sp_skill_evolution_2] = "SP技能2+"
    if skill.sp_skill_3:
        skill_dict["sp"].append(skill.sp_skill_3)
        skill_type_dict[skill.sp_skill_3] = "SP技能3"
    if skill.sp_skill_4:
        skill_dict["sp"].append(skill.sp_skill_4)
        skill_type_dict[skill.sp_skill_4] = "SP技能4"
    if skill.sp_skill_5:
        skill_dict["sp"].append(skill.sp_skill_5)
        skill_type_dict[skill.sp_skill_5] = "SP技能5"

    return skill_dict, skill_type_dict


def get_action_description(
    action_data: List[SkillActionData],
    skill_data: SkillData,
    level: int = 0,
    atk: int = 0,
) -> List[SkillActionText]:
    action_text_list = []
    summon_unit_id = 0
    for action in action_data:
        if action.action_type == SkillActionType.SUMMON.value:
            summon_unit_id = action.action_detail_2
        # 生成技能效果文本
        desc = action_handler.format_desc(action, skill_data, level, atk)
        # 是否显示系数判断
        show_coe = action.action_type in (
            SkillActionType.ADDITIVE.value,
            SkillActionType.MULTIPLE.value,
            SkillActionType.DIVIDE.value,
            SkillActionType.RATE_DAMAGE.value,
        )
        action_text_list.append(
            SkillActionText(
                actionId=action.action_id,
                tag=StringResources.get(
                    SKILL_DESCRIPTIONS.get(action.action_type, "none")
                )
                or action_handler.tag,
                action_desc=f"({action.action_id % 100}) {desc}",
                summon_unit_id=summon_unit_id,
                show_coe=show_coe,
            )
        )
    return action_text_list


def get_action_index_with_coe(actions: List[SkillActionText]) -> List[ShowCoe]:
    list_result = []
    try:
        for index, action_desc in enumerate(actions):
            if action_desc.show_coe:
                coe_match = re.findall(r"\{.\}", action_desc.action_desc)
                coe = coe_match[0] if coe_match else None

                if coe:
                    list_result.append(ShowCoe(index, 0, coe))

                    action_text = StringResources.get("skill_action")
                    pattern = rf"{action_text}\(.+\)"
                    for result in re.findall(pattern, action_desc.action_desc):
                        next_index = int(result[3]) - 1  # 提取括号中的数字并转换为索引
                        list_result.append(ShowCoe(next_index, 1, coe))
    except Exception as e:
        print(f"Exception occurred: {e}")

    return list_result


def process_action_data(action_data: List[SkillActionText]):
    try:
        show_coe_index = get_action_index_with_coe(action_data)
        for index, skill_action_text in enumerate(action_data):
            # 筛选出当前索引对应的 ShowCoe 对象
            s = [item for item in show_coe_index if item.action_index == index]
            show = len(s) > 0  # 是否需要显示系数
            action_desc = skill_action_text.action_desc

            if show:
                # 查找系数表达式的起始位置
                start_index = action_desc.find("<")
                if start_index == -1:
                    start_index = action_desc.find("[")

                if start_index != -1:
                    coe_expr = action_desc[start_index:]

                    # 查找所有 `{}` 中的内容
                    for match in re.findall(r"\{.*?\}", skill_action_text.action_desc):
                        if s[0].coe_type == 0 or (
                            s[0].coe_type == 1 and s[0].coe != match
                        ):
                            # 隐藏不需要的系数文本
                            coe_expr = coe_expr.replace(match, "")

                    # 更新 action_desc
                    skill_action_text.action_desc = action_desc[:start_index] + coe_expr
            else:
                # 隐藏所有 `{}` 中的内容
                skill_action_text.action_desc = re.sub(r"\{.*?\}", "", action_desc)

    except Exception as e:
        print(f"Exception occurred: {e}")


def get_atk_type(action_detail_1: int) -> str:
    if action_detail_1 == 1:
        return "物理"
    elif action_detail_1 == 2:
        return "魔法"
    elif action_detail_1 == 3:
        return "必定命中的物理"
    elif action_detail_1 == 4:
        return "必定命中的魔法"
    elif action_detail_1 == 5:
        return "(物理、魔法攻击力合计)物理"
    elif action_detail_1 == 6:
        return "(物理、魔法攻击力合计)魔法"
    else:
        return "未知"


def get_barrier_type(v1):
    # 作用
    if v1 in [1, 2, 5]:
        f = StringResources.get("skill_shield_no_effect")
    else:
        f = StringResources.get("skill_shield_defense")

    # 类型
    if v1 in [1, 3]:
        type_ = StringResources.get("physical")
    elif v1 in [2, 4]:
        type_ = StringResources.get("magic")
    else:
        type_ = StringResources.get("skill_all")

    return StringResources.get("skill_shield", f, type_) if v1 <= 6 else "UNKNOWN"


def init_other_limit():
    return  # FIXME 用不上
    # if self.level > 100 and self.is_other_rf_skill:  # 100 作为示例的阈值
    # self.is_other_limit_action = True


def get_aura(v, value_text):
    action = StringResources.get(
        "skill_hp_max"
        if v == 1
        else {
            1: "attr_atk",
            2: "attr_def",
            3: "attr_magic_str",
            4: "attr_magic_def",
            5: "attr_dodge",
            6: "attr_physical_critical",
            7: "attr_magic_critical",
            8: "attr_energy_recovery_rate",
            9: "attr_life_steal",
            10: "skill_speed",
            11: "skill_physical_critical_damage",
            12: "skill_magic_critical_damage",
            13: "attr_accuracy",
            14: "skill_critical_damage_take",
            16: "skill_physical_damage_take",
            17: "skill_magic_damage_take",
            18: "skill_physical_damage",
            19: "skill_magic_damage",
        }.get(v % 1000 // 10, "unknown")
    )

    if v // 10 in [14, 16, 17]:
        type_ = (
            StringResources.get("skill_reduce" if v % 10 == 0 else "skill_increase")
            + " "
            + value_text
        )
    else:
        type_ = (
            StringResources.get("skill_increase" if v % 10 == 0 else "skill_reduce")
            + " "
            + value_text
        )

    # 固定buff，不受其他效果影响
    if v > 1000:
        type_ += StringResources.get("skill_fixed")

    return action + type_


def get_status(value, action_value_3):
    return StringResources.get(
        {
            100: "skill_status_100",
            101: "skill_status_101",
            200: "skill_status_200",
            300: "skill_status_300",
            400: "skill_status_400",
            500: "skill_status_500",
            501: "skill_status_501",
            502: "skill_status_502",
            503: "skill_status_503",
            504: "skill_status_504",
            511: "skill_status_511",
            512: "skill_status_512",
            710: "skill_status_710",
            900: "skill_status_900",
            1400: "skill_status_1400",
            1600: "skill_status_1600",
            1601: "skill_status_1601",
            1700: {21: "skill_status_1700_21", 41: "skill_status_1700_41"}.get(
                action_value_3, "unknown"
            ),
            721: "skill_status_721",
            6107: "skill_status_6107",
            1513: "skill_ailment_13",
            1800: "skill_status_1800",
            1900: "skill_status_1900",
            3137: "skill_status_3137",
            3162: "skill_status_3162",
            3175: "skill_status_3175",
            3207: "skill_status_3207",
            6160: "skill_status_6160",
            4001: "skill_target_fire",
            4002: "skill_target_waterAdd commentMore actions",
            4003: "skill_target_wind",
            4004: "skill_target_light",
            4005: "skill_target_dark",
        }.get(value, "unknown")
    )


def get_skill_depend_dict(skill_data: SkillData):
    return {
        skill_data.action_1: skill_data.depend_action_1,
        skill_data.action_2: skill_data.depend_action_2,
        skill_data.action_3: skill_data.depend_action_3,
        skill_data.action_4: skill_data.depend_action_4,
        skill_data.action_5: skill_data.depend_action_5,
        skill_data.action_6: skill_data.depend_action_6,
        skill_data.action_7: skill_data.depend_action_7,
        skill_data.action_8: skill_data.depend_action_8,
        skill_data.action_9: skill_data.depend_action_9,
        skill_data.action_10: skill_data.depend_action_10,
    }


class ActionHandler:

    def __init__(self):
        self.action_msg_func = {
            SkillActionType.DAMAGE.value: self.damage,
            SkillActionType.MOVE.value: self.move,
            SkillActionType.CHANGE_ENEMY_POSITION.value: self.change_position,
            SkillActionType.HEAL.value: self.heal,
            SkillActionType.BARRIER.value: self.barrier,
            SkillActionType.CHOOSE_ENEMY.value: self.choose_enemy,
            SkillActionType.CHANGE_ACTION_SPEED.value: self.speed,
            SkillActionType.SUPERIMPOSE_CHANGE_ACTION_SPEED.value: self.speed,
            SkillActionType.SPEED_FIELD.value: self.speed,
            SkillActionType.DOT.value: self.dot,
            SkillActionType.AURA.value: self.aura,
            SkillActionType.AURA_V2.value: self.aura,
            SkillActionType.CHARM.value: self.charm,
            SkillActionType.BLIND.value: self.charm,
            SkillActionType.SILENCE.value: self.charm,
            SkillActionType.CHANGE_MODE.value: self.change_mode,
            SkillActionType.SUMMON.value: self.summon,
            SkillActionType.CHANGE_TP.value: self.tp,
            SkillActionType.TRIGGER.value: self.trigger,
            SkillActionType.TRIGGER_V2.value: self.trigger_v2,
            SkillActionType.CHARGE.value: self.charge,
            SkillActionType.DAMAGE_CHARGE.value: self.charge,
            SkillActionType.TAUNT.value: self.taunt,
            SkillActionType.INVINCIBLE.value: self.invincible,
            SkillActionType.CHANGE_PATTERN.value: self.change_pattern,
            SkillActionType.IF_STATUS.value: self.if_status,
            SkillActionType.REVIVAL.value: self.revival,
            SkillActionType.ADDITIVE.value: self.coefficient,
            SkillActionType.MULTIPLE.value: self.coefficient,
            SkillActionType.DIVIDE.value: self.coefficient,
            SkillActionType.IF_SP_STATUS.value: self.if_sp_status,
            SkillActionType.NO_UB.value: self.no_ub,
            SkillActionType.KILL_ME.value: self.kill_me,
            SkillActionType.LIFE_STEAL.value: self.life_steal,
            SkillActionType.STRIKE_BACK.value: self.strike_back,
            SkillActionType.ACCUMULATIVE_DAMAGE.value: self.accumulative_damage,
            SkillActionType.ACCUMULATIVE_DAMAGE_V2.value: self.accumulative_damage,
            SkillActionType.SEAL.value: self.seal,
            SkillActionType.SEAL_V2.value: self.seal_v2,
            SkillActionType.ATTACK_FIELD.value: self.attack_field,
            SkillActionType.HEAL_FIELD.value: self.heal_field,
            SkillActionType.AURA_FIELD.value: self.aura_field,
            SkillActionType.DOT_FIELD.value: self.dot_field,
            SkillActionType.LOOP_TRIGGER.value: self.loop_trigger,
            SkillActionType.WAVE_START.value: self.wave_start,
            SkillActionType.SKILL_COUNT.value: self.skill_count,
            SkillActionType.RATE_DAMAGE.value: self.rate_damage,
            SkillActionType.UPPER_LIMIT_ATTACK.value: self.limit_attack,
            SkillActionType.HOT.value: self.hot,
            SkillActionType.DISPEL.value: self.dispel,
            SkillActionType.CHANNEL.value: self.channel,
            SkillActionType.CHANGE_WIDTH.value: self.change_width,
            SkillActionType.IF_HAS_FIELD.value: self.if_has_field,
            SkillActionType.STEALTH.value: self.stealth,
            SkillActionType.MOVE_PART.value: self.move_part,
            SkillActionType.COUNT_BLIND.value: self.count_blind,
            SkillActionType.COUNT_DOWN.value: self.count_down,
            SkillActionType.STOP_FIELD.value: self.stop_field,
            SkillActionType.INHIBIT_HEAL_ACTION.value: self.inhibit_heal,
            SkillActionType.ATTACK_SEAL.value: self.attack_seal,
            SkillActionType.FEAR.value: self.fear,
            SkillActionType.AWE.value: self.awe,
            SkillActionType.LOOP.value: self.loop,
            SkillActionType.REINDEER.value: self.reindeer,
            SkillActionType.EXEMPTION_DEATH.value: self.exemption_death,
            SkillActionType.DAMAGE_REDUCE.value: self.damage_reduce,
            SkillActionType.LOG_BARRIER.value: self.log_barrier,
            SkillActionType.HIT_COUNT.value: self.hit_count,
            SkillActionType.HEAL_DOWN.value: self.heal_down,
            SkillActionType.IF_BUFF_SEAL.value: self.if_buff_seal,
            SkillActionType.DMG_TAKEN_UP.value: self.damage_taken_up,
            SkillActionType.ACTION_DOT.value: self.action_dot,
            SkillActionType.NO_TARGET.value: self.no_target,
            SkillActionType.EX.value: self.ex,
            SkillActionType.EX_EQUIP.value: self.ex_equip_full,
            SkillActionType.EX_EQUIP_HALF.value: self.ex_equip_half,
            SkillActionType.CHANGE_TP_RATIO.value: self.change_tp_ratio,
            SkillActionType.IGNORE_TAUNT.value: self.ignore_taunt,
            SkillActionType.SPECIAL_EFFECT.value: self.special_effect,
            SkillActionType.HIDE.value: self.hide,
            SkillActionType.TP_FIELD.value: self.tp_field,
            SkillActionType.TP_HIT.value: self.tp_hit,
            SkillActionType.TP_HIT_REDUCE.value: self.tp_hit_reduce,
            SkillActionType.IGNORE_SPEED_DOWN.value: self.ignore_speed_down,
            SkillActionType.COPY_ATK.value: self.copy_atk,
            SkillActionType.ENVIRONMENT.value: self.environment,
            SkillActionType.GUARD.value: self.guard,
            SkillActionType.SUM_CRITICAL.value: self.sum_critical,
            SkillActionType.DOT_UP.value: self.dot_up,
            SkillActionType.SEAL_COUNT.value: self.seal_count,
            SkillActionType.PERSISTENT.value: self.persistent,
            SkillActionType.MAGIC_CHANGE.value: self.magic_change,
            SkillActionType.MAGIC_CHANGE_REDUCE_DAMAGE.value: self.magic_change_reduce_damage,
            SkillActionType.TRANSFER_DAMAGE.value: self.transfer_damage,
            SkillActionType.CANNOT_SELECTED.value: self.cannot_selected,
            SkillActionType.BUFF_DOT.value: self.buff_dot,
            SkillActionType.DAMAGE_TO_DOT.value: self.damage2dot,
            SkillActionType.CHANGE_DEF_MAX.value: self.change_def_max,
        }

    def format_desc(
        self,
        action: SkillActionData,
        skill_data: SkillData,
        level: int = 0,
        atk: int = 0,
    ) -> str:
        self.level = level
        self.atk = atk
        self.action = action
        self.skill_data = skill_data
        self.tag = ""
        if action.action_type not in self.action_msg_func:
            print(self.action.action_type, "not in action_msg_func")
            return self.unknown_type()
        return self.action_msg_func[action.action_type]()

    def unknown_type(self):
        value = self.get_value_text(
            1, self.action.action_value_1, self.action.action_value_2, percent="%"
        )
        time = self.get_time_text(
            3, self.action.action_value_3, self.action.action_value_4
        )
        print(
            StringResources.get(
                "skill_action_type_unknown",
                self.get_target(),
                self.action.ailment_name,
                self.action.action_type,
                value,
                time,
            )
        )
        return StringResources.get(
            "skill_action_type_unknown",
            self.get_target(),
            self.action.ailment_name,
            self.action.action_type,
            value,
            time,
        )

    def transfer_damage(self):
        time = self.get_time_text(3, self.action.action_value_3)
        status = StringResources.get("skill_action_type_124")
        return StringResources.get(
            "skill_action_type_desc_116_121_123_124", self.get_target(), status, time
        )

    def magic_change(self):
        time = self.get_time_text(5, self.action.action_value_5)
        status = StringResources.get("skill_action_type_121")
        return StringResources.get(
            "skill_action_type_desc_116_121_123_124", self.get_target(), status, time
        )

    def magic_change_reduce_damage(self):
        time = self.get_time_text(3, self.action.action_value_3)
        value = self.get_value_text(
            1, self.action.action_value_1, self.action.action_value_2, percent="%"
        )
        desc = StringResources.get("skill_action_type_desc_123_1", value)
        return StringResources.get(
            "skill_action_type_desc_116_121_123_124", self.get_target(), desc, time
        )

    def persistent(self):
        time = self.get_time_text(1, self.action.action_value_1)
        status = StringResources.get("skill_action_type_116")
        return StringResources.get(
            "skill_action_type_desc_116_121_123_124", self.get_target(), status, time
        )

    def sum_critical(self):
        return StringResources.get(
            "skill_action_type_desc_107", self.action.action_detail_1 % 100
        )

    def guard(self):
        type_ = {
            141: StringResources.get("skill_action_type_desc_106_type_141"),
        }.get(
            self.action.action_detail_1,
            StringResources.get("skill_action_type_desc_106_type_common"),
        )
        time = self.get_time_text(
            3, self.action.action_value_3, self.action.action_value_4
        )
        return StringResources.get(
            "skill_action_type_desc_106", self.get_target(), type_, time
        )

    # 105：环境效果
    def environment(self):
        type_ = {
            137: StringResources.get("skill_status_3137"),
            162: StringResources.get("skill_status_3162"),
            175: StringResources.get("skill_status_3175"),
            207: StringResources.get("skill_status_3207"),
        }.get(self.action.action_detail_2, StringResources.get("unknown"))

        time = self.get_time_text(1, self.action.action_value_1)
        return StringResources.get("skill_action_type_desc_105", type_, time)

    def copy_atk(self):
        return StringResources.get(
            "skill_action_type_desc_103",
            self.action.action_detail_2 % 100,
            self.get_target(),
        )

    def hide(self):
        time = self.get_time_text(
            1, self.action.action_value_1, self.action.action_value_2
        )
        return StringResources.get("skill_action_type_desc_95", self.get_target(), time)

    def special_effect(self):
        return StringResources.get("skill_action_type_desc_94", self.get_target())

    def ex_equip_full(self):
        return StringResources.get("skill_action_type_desc_901")

    def ex_equip_half(self):
        return StringResources.get(
            "skill_action_type_desc_902", self.action.action_value_3
        )

    # 90：EX被动
    def ex(self):
        type_ = {
            1: StringResources.get("attr_hp"),
            2: StringResources.get("attr_atk"),
            3: StringResources.get("attr_def"),
            4: StringResources.get("attr_magic_str"),
            5: StringResources.get("attr_magic_def"),
            6: StringResources.get("attr_physical_critical"),
            7: StringResources.get("attr_magic_critical"),
        }.get(self.action.action_detail_1, "UNKNOWN")

        value = self.get_value_text(
            2, self.action.action_value_2, self.action.action_value_3
        )

        return StringResources.get(
            "skill_action_type_desc_90", self.get_target(), type_, value
        )

    def no_target(self):
        return StringResources.get("skill_action_type_desc_81", self.get_target())

    # 75：次数触发
    def hit_count(self):
        time = self.get_time_text(
            3, self.action.action_value_3, self.action.action_value_4
        )

        if self.action.action_detail_1 == 3:
            return StringResources.get(
                "skill_action_type_desc_75",
                self.action.action_value_1,
                self.action.action_detail_2 % 100,
                time,
            )
        else:
            return "UNKNOWN"

    # 78：被击伤害上升
    def damage_taken_up(self):
        time = self.get_time_text(
            3, self.action.action_value_3, self.action.action_value_4
        )
        limit = StringResources.get(
            "skill_action_limit_int", self.action.action_value_2
        )
        # 数量类型
        count_type = {1: StringResources.get("skill_action_type_desc_78_1")}.get(
            self.action.action_detail_1, StringResources.get("unknown")
        )
        # 增加或减少
        effect_type = {
            1: StringResources.get("skill_action_type_desc_additive"),
            2: StringResources.get("skill_action_type_desc_subtract"),
        }.get(self.action.action_detail_2, StringResources.get("unknown"))
        # 倍数计算公式
        value_text = f"<{self.action.action_value_1} * {count_type}>"
        return StringResources.get(
            "skill_action_type_desc_78",
            self.get_target(),
            effect_type,
            value_text,
            time,
            limit,
        )

    # 72：伤害减免
    def damage_reduce(self):
        type_ = {
            1: StringResources.get("skill_physical"),
            2: StringResources.get("skill_magic"),
            3: StringResources.get("skill_all"),
        }.get(self.action.action_detail_1, "UNKNOWN")
        value = self.get_value_text(
            1, self.action.action_value_1, self.action.action_value_2, percent="%"
        )
        time = self.get_time_text(
            3, self.action.action_value_3, self.action.action_value_4
        )
        return StringResources.get(
            "skill_action_type_desc_72", self.get_target(), type_, value, time
        )

    def exemption_death(self):

        return StringResources.get(
            "skill_action_type_desc_71",
            self.get_target(),
            self.get_value_text(
                2,
                self.action.action_value_2,
                self.action.action_value_3,
                self.action.action_value_4,
            ),
            self.get_time_text(
                6, self.action.action_value_6, self.action.action_value_7
            ),
        )

    def reindeer(self):
        return StringResources.get(
            "skill_action_type_desc_69",
            self.get_target(),
            self.get_time_text(
                1, self.action.action_value_1, self.action.action_value_2
            ),
        )

    # 63: 循环动作
    def loop(self):
        success_clause = (
            StringResources.get(
                "skill_action_type_desc_63_success", self.action.action_detail_2 % 100
            )
            if self.action.action_detail_2 != 0
            else "UNKNOWN"
        )
        failure_clause = (
            StringResources.get(
                "skill_action_type_desc_63_failure", self.action.action_detail_3 % 100
            )
            if self.action.action_detail_3 != 0
            else "UNKNOWN"
        )
        main = StringResources.get(
            "skill_action_type_desc_63",
            self.action.action_value_2,
            self.action.action_detail_1 % 100,
            self.action.action_value_1,
            self.action.action_value_3,
        )

        if success_clause != "UNKNOWN" and failure_clause != "UNKNOWN":
            return main + success_clause + failure_clause
        elif success_clause != "UNKNOWN":
            return main + success_clause
        elif failure_clause != "UNKNOWN":
            return main + failure_clause
        else:
            return "UNKNOWN"

    def awe(self):
        value = self.get_value_text(
            1, self.action.action_value_1, self.action.action_value_2, 0.0, percent="%"
        )
        time = self.get_time_text(
            3, self.action.action_value_3, self.action.action_value_4
        )
        return {
            0: StringResources.get(
                "skill_action_type_desc_62_0", self.get_target(), value, time
            ),
            1: StringResources.get(
                "skill_action_type_desc_62_1", self.get_target(), value, time
            ),
        }.get(self.action.action_detail_1, "UNKNOWN")

    # 61：恐慌
    def fear(self):
        value = self.get_value_text(
            3, self.action.action_value_3, self.action.action_value_4, 0.0, percent="%"
        )
        time = self.get_time_text(
            1, self.action.action_value_1, self.action.action_value_2
        )
        return StringResources.get(
            "skill_action_type_desc_61",
            value,
            self.get_target(),
            self.action.ailment_name,
            time,
        )

    def count_down(self):
        return StringResources.get(
            "skill_action_type_desc_57",
            self.get_target(),
            self.action.action_value_1,
            self.action.action_detail_1 % 100,
        )

    def count_blind(self):
        if self.action.action_value_1 == 1:
            time = self.get_time_text(
                2, self.action.action_value_2, self.action.action_value_3
            )
            return StringResources.get("skill_action_type_desc_56_1", time)
        elif self.action.action_value_1 == 2:
            value = self.get_value_text(
                2, self.action.action_value_2, self.action.action_value_3
            )
            return StringResources.get(
                "skill_action_type_desc_56_2", self.get_target(), value
            )
        else:
            return "UNKNOWN"

    def move_part(self):
        return StringResources.get(
            "skill_action_type_desc_55",
            self.action.action_value_4,
            -self.action.action_value_1,
        )

    def stealth(self):
        return StringResources.get(
            "skill_action_type_desc_54",
            self.get_time_text(1, self.action.action_value_1),
        )

    def change_width(self):
        return StringResources.get("skill_action_type_desc_52")

    # 50：持续动作
    def channel(self):
        time = self.get_time_text(
            4, self.action.action_value_4, self.action.action_value_5
        )
        value = self.get_value_text(
            2,
            self.action.action_value_2,
            self.action.action_value_3,
            percent=self.get_percent(),
        )
        aura = get_aura(self.action.action_detail_1, value)
        return StringResources.get(
            "skill_action_type_desc_50",
            self.get_target(),
            aura,
            time,
            self.action.action_detail_3,
        )

    # 49：移除增益
    def dispel(self):
        value = self.get_value_text(
            1, self.action.action_value_1, self.action.action_value_2, 0.0, percent="%"
        )
        type_ = {
            1: StringResources.get("skill_buff"),
            3: StringResources.get("skill_buff"),
            2: StringResources.get("skill_debuff"),
            10: StringResources.get("skill_barrier"),
            20: StringResources.get("skill_barrier"),
        }.get(self.action.action_detail_1, "UNKNOWN")

        return StringResources.get(
            "skill_action_type_desc_49", value, self.get_target(), type_
        )

    # 48：持续治疗
    def hot(self):
        type_ = {
            1: StringResources.get("attr_hp"),
            2: StringResources.get("attr_tp"),
        }.get(self.action.action_detail_2, "UNKNOWN")

        value = self.get_value_text(
            1,
            self.action.action_value_1,
            self.action.action_value_2,
            self.action.action_value_3,
        )
        time = self.get_time_text(
            5, self.action.action_value_5, self.action.action_value_6
        )

        if type_ != "UNKNOWN":
            return StringResources.get(
                "skill_action_type_desc_48", self.get_target(), type_, value, time
            )
        else:
            return "UNKNOWN"

    def limit_attack(self):
        return StringResources.get("skill_action_type_desc_47")

    def skill_count(self):
        return StringResources.get(
            "skill_action_type_desc_45",
            StringResources.get("skill_action_limit_int", self.action.action_value_1),
        )

    def wave_start(self):
        return StringResources.get(
            "skill_action_type_desc_44", self.action.action_value_1
        )

    # 36：攻击领域展开
    def attack_field(self):
        atk_type = get_atk_type(self.action.action_detail_1)
        value = self.get_value_text(
            1,
            self.action.action_value_1,
            self.action.action_value_2,
            self.action.action_value_3,
        )
        time = self.get_time_text(
            5, self.action.action_value_5, self.action.action_value_6
        )
        damage = StringResources.get(
            "skill_action_type_desc_36_damage", value, atk_type
        )
        return StringResources.get(
            "skill_action_type_desc_field",
            self.action.action_value_7,
            damage,
            time,
        )

    # 37：治疗领域展开
    def heal_field(self):
        value = self.get_value_text(
            1,
            self.action.action_value_1,
            self.action.action_value_2,
            self.action.action_value_3,
        )
        heal = StringResources.get("skill_action_type_desc_37_heal", value)
        time = self.get_time_text(
            5, self.action.action_value_5, self.action.action_value_6
        )
        return StringResources.get(
            "skill_action_type_desc_field", self.action.action_value_7, heal, time
        )

    # 38：buff/debuff领域展开
    def aura_field(self):
        value = self.get_value_text(
            1,
            self.action.action_value_1,
            self.action.action_value_2,
            percent=self.get_percent(),
        )
        time = self.get_time_text(
            3, self.action.action_value_3, self.action.action_value_4
        )
        aura = get_aura(self.action.action_detail_1, value)
        return self.get_target() + StringResources.get(
            "skill_action_type_desc_field", self.action.action_value_5, aura, time
        )

    # 39：持续伤害领域展开
    def dot_field(self):
        time = self.get_time_text(
            1, self.action.action_value_1, self.action.action_value_2
        )
        action = StringResources.get(
            "skill_action_type_desc_38_action", self.action.action_detail_1 % 100
        )
        return self.get_target() + StringResources.get(
            "skill_action_type_desc_field",
            self.action.action_value_3,
            action,
            time,
        )

    # 53：特殊状态：领域存在时；如：情姐
    def if_has_field(self):
        if self.action.action_detail_2 != 0 and self.action.action_detail_3 != 0:
            otherwise = StringResources.get(
                "skill_action_type_desc_53_2", self.action.action_detail_3 % 100
            )
            content = StringResources.get(
                "skill_action_type_desc_53",
                self.action.action_detail_2 % 100,
                otherwise,
            )
        elif self.action.action_detail_2 != 0:
            content = StringResources.get(
                "skill_action_type_desc_53", self.action.action_detail_2 % 100, ""
            )
        else:
            content = "UNKNOWN"
        return StringResources.get("skill_action_condition", content)

    # 58：解除领域 如：晶姐 UB
    def stop_field(self):
        return StringResources.get(
            "skill_action_type_desc_58",
            self.action.action_detail_1 // 100 % 10,
            self.action.action_detail_1 % 100,
        )

    # 96：范围tp回复
    def tp_field(self):
        value = self.get_value_text(
            1, self.action.action_value_1, self.action.action_value_2
        )
        tp = StringResources.get("skill_action_type_desc_96_tp", value)
        time = self.get_time_text(
            3, self.action.action_value_3, self.action.action_value_4
        )
        return StringResources.get(
            "skill_action_type_desc_field", self.action.action_value_5, tp, time
        )

    # 35：特殊标记
    def seal(self):
        count = abs(self.action.action_value_4)
        if self.action.action_value_4 <= 0:
            return StringResources.get(
                "skill_action_type_desc_35_reduce", self.get_target(), count
            )
        time = self.get_time_text(3, self.action.action_value_3, hide_index=True)
        limit = StringResources.get(
            "skill_action_limit_int", self.action.action_value_1
        )
        return StringResources.get(
            "skill_action_type_desc_35", self.get_target(), count, time, limit
        )

    # 60：标记赋予
    def attack_seal(self):
        limit = StringResources.get(
            "skill_action_limit_int", self.action.action_value_1
        )
        time = self.get_time_text(
            3, self.action.action_value_3, self.action.action_value_4
        )
        target = self.get_target()
        desc = StringResources.get("skill_action_type_desc_60_0", time, limit)

        if self.action.action_detail_1 == 3:
            return StringResources.get("skill_action_type_desc_60_1", target, desc)
        elif self.action.action_detail_1 == 1 and self.action.action_detail_3 == 1:
            return StringResources.get("skill_action_type_desc_60_2", target, desc)
        elif self.action.action_detail_1 == 4 and self.action.action_detail_3 == 1:
            return StringResources.get("skill_action_type_desc_60_3", target, desc)
        elif self.action.action_detail_1 == 5 and self.action.action_detail_3 == 1:
            return StringResources.get("skill_action_type_desc_60_4", target, desc)
        else:
            return "UNKNOWN"

    # 77：被动叠加标记
    def if_buff_seal(self):
        time = self.get_time_text(
            3, self.action.action_value_3, self.action.action_value_4
        )
        effect = {
            1: StringResources.get("skill_action_type_desc_77_1")
            + StringResources.get("skill_buff"),
            2: StringResources.get("skill_action_type_desc_77_1")
            + StringResources.get("skill_damage"),
            3: StringResources.get("skill_action_type_desc_77_1")
            + StringResources.get("skill_status_down"),
            4: StringResources.get("skill_status_ub"),
        }.get(self.action.action_detail_1, "UNKNOWN")
        limit = StringResources.get(
            "skill_action_limit_int", self.action.action_value_1
        )

        return StringResources.get(
            "skill_action_type_desc_77",
            self.get_target() if (self.action.action_detail_1 != 4) else "",
            effect,
            self.action.action_detail_2,
            time,
            limit,
        )

    # 101：特殊标记v2
    def seal_v2(self):
        count = abs(self.action.action_detail_2)
        if self.action.action_detail_2 < 0:
            return StringResources.get(
                "skill_action_type_desc_101_reduce", self.get_target(), count
            )
        time = self.get_time_text(3, self.action.action_value_3, hide_index=True)
        limit = StringResources.get(
            "skill_action_limit_int", self.action.action_value_1
        )
        return StringResources.get(
            "skill_action_type_desc_101", self.get_target(), count, time, limit
        )

    # 114：特殊标记计数？
    def seal_count(self):
        action1 = self.action.action_detail_1 % 100
        action2 = self.action.action_detail_2 % 100
        time = self.get_time_text(4, self.action.action_value_4, hide_index=True)
        aura = StringResources.get(
            "skill_action_type_desc_114_aura", self.action.action_value_3
        )

        return StringResources.get(
            "skill_action_type_desc_114",
            self.get_target(),
            self.action.action_value_2,
            aura,
            action1,
            action2,
            time,
        )

    # 46：比例伤害
    def rate_damage(self):
        value = self.get_value_text(
            1, self.action.action_value_1, self.action.action_value_2, percent="%"
        )
        limit = StringResources.get(
            "skill_action_damage_limit_int", self.action.action_value_3
        )
        result = {
            1: StringResources.get(
                "skill_action_type_desc_46_1", self.get_target(), value
            ),
            2: StringResources.get(
                "skill_action_type_desc_46_2", self.get_target(), value
            ),
            3: StringResources.get(
                "skill_action_type_desc_46_3", self.get_target(), value
            ),
        }.get(self.action.action_detail_1, "UNKNOWN")
        return result + (limit if self.action.action_value_3 != 0.0 else "")

    # 34、102：伤害递增
    def accumulative_damage(self):
        value = self.get_value_text(
            2, self.action.action_value_2, self.action.action_value_3
        )
        limit = StringResources.get(
            "skill_action_limit_int", self.action.action_value_4
        )
        return StringResources.get("skill_action_type_desc_34", value, limit)

    # 33：反伤
    def strike_back(self):
        value = self.get_value_text(
            1, self.action.action_value_1, self.action.action_value_2
        )
        type_ = get_barrier_type(self.action.action_detail_1)
        shield_text = StringResources.get(
            "skill_action_type_desc_6", self.get_target(), type_, "", ""
        )

        back_type = {
            1: StringResources.get("skill_physical"),
            3: StringResources.get("skill_physical"),
            2: StringResources.get("skill_magic"),
            4: StringResources.get("skill_magic"),
        }.get(self.action.action_detail_1, "")

        hp_recovery = {
            3: StringResources.get("skill_action_type_desc_33_hp"),
            4: StringResources.get("skill_action_type_desc_33_hp"),
            6: StringResources.get("skill_action_type_desc_33_hp"),
        }.get(self.action.action_detail_1, "")

        if self.action.action_detail_1 <= 6:
            return StringResources.get(
                "skill_action_type_desc_33",
                shield_text,
                back_type,
                value,
                hp_recovery,
                self.action.action_value_3,
            )
        else:
            return "UNKNOWN"

    # 32：HP吸收
    def life_steal(self):
        # 回避等技能限制
        init_other_limit()
        value = self.get_value_text(
            1, self.action.action_value_1, self.action.action_value_2
        )
        return StringResources.get(
            "skill_action_type_desc_32",
            self.get_target(),
            self.action.action_value_3,
            self.action.ailment_name,
            value,
        )

    def kill_me(self):
        return StringResources.get("skill_action_type_desc_30", self.get_target())

    def no_ub(self):
        return StringResources.get("skill_action_type_desc_29")

    # 28：特殊条件
    def if_sp_status(self):
        status = get_status(self.action.action_detail_1, self.action.action_value_3)
        true_clause = "UNKNOWN"
        false_clause = "UNKNOWN"
        # 对应 Kotlin：if (self.action.action_detail_2 != 0 || self.action.action_detail_3 == 0) {...}
        if self.action.action_detail_2 != 0 or self.action.action_detail_3 == 0:
            if 0 <= self.action.action_detail_1 <= 99:
                # skill_action_sp_if_rate
                true_clause = StringResources.get(
                    "skill_action_sp_if_rate",
                    self.action.action_detail_1,
                    self.action.action_detail_2 % 100,
                )
            elif self.action.action_detail_1 == 599:
                # skill_action_sp_if_dot
                true_clause = StringResources.get(
                    "skill_action_sp_if_dot",
                    self.get_target(),
                    self.action.action_detail_2 % 100,
                )
            elif (600 <= self.action.action_detail_1 <= 699) or (
                6000 <= self.action.action_detail_1 <= 6999
            ):
                # skill_action_sp_if_mark_count
                cnt = max(int(self.action.action_value_3), 1)
                true_clause = StringResources.get(
                    "skill_action_sp_if_mark_count",
                    self.get_target(),
                    cnt,
                    self.action.action_detail_2 % 100,
                )
            elif self.action.action_detail_1 == 700:
                # skill_action_if_alone
                true_clause = StringResources.get(
                    "skill_action_if_alone",
                    self.get_target(),
                    self.action.action_detail_2 % 100,
                )
            elif 701 <= self.action.action_detail_1 <= 709:
                # skill_action_sp_if_unit_count
                true_clause = StringResources.get(
                    "skill_action_sp_if_unit_count",
                    self.get_target(),
                    self.action.action_detail_1 - 700,
                    self.action.action_detail_2 % 100,
                )
            elif self.action.action_detail_1 == 720:
                # skill_action_sp_if_unit_exist
                true_clause = StringResources.get(
                    "skill_action_sp_if_unit_exist",
                    self.get_target(),
                    self.action.action_detail_2 % 100,
                )
            elif 901 <= self.action.action_detail_1 <= 999:
                # skill_action_if_hp_below
                true_clause = StringResources.get(
                    "skill_action_if_hp_below",
                    self.get_target(),
                    self.action.action_detail_1 - 900,
                    self.action.action_detail_2 % 100,
                )
            elif self.action.action_detail_1 == 1000:
                # skill_action_sp_if_kill
                true_clause = StringResources.get(
                    "skill_action_sp_if_kill", self.action.action_detail_2 % 100
                )
            elif self.action.action_detail_1 == 1001:
                # skill_action_sp_if_critical
                true_clause = StringResources.get(
                    "skill_action_sp_if_critical", self.action.action_detail_2 % 100
                )
            elif 1200 <= self.action.action_detail_1 <= 1299:
                # skill_action_sp_if_skill_count
                true_clause = StringResources.get(
                    "skill_action_sp_if_skill_count",
                    self.get_target(),
                    self.action.action_detail_1 % 10,
                    self.action.action_detail_2 % 100,
                )
            elif (
                self.action.action_detail_1 == 2000
                or self.action.action_detail_1 == 1300
            ):
                # skill_action_if_unit_atk_type ... physical
                true_clause = StringResources.get(
                    "skill_action_if_unit_atk_type",
                    self.get_target(),
                    StringResources.get("skill_status_physical_atk"),
                    self.action.action_detail_2 % 100,
                )
            elif self.action.action_detail_1 == 2001:
                # skill_action_if_unit_atk_type ... magic
                true_clause = StringResources.get(
                    "skill_action_if_unit_atk_type",
                    self.get_target(),
                    StringResources.get("skill_status_magic_atk"),
                    self.action.action_detail_2 % 100,
                )
            else:
                # skill_action_if_status
                true_clause = StringResources.get(
                    "skill_action_if_status",
                    self.get_target(),
                    status,
                    self.action.action_detail_2 % 100,
                )

        # 对应 Kotlin：if (self.action.action_detail_3 != 0) {...}
        if self.action.action_detail_3 != 0:
            if 0 <= self.action.action_detail_1 <= 99:
                # skill_action_sp_if_rate
                false_clause = StringResources.get(
                    "skill_action_sp_if_rate",
                    100 - self.action.action_detail_1,
                    self.action.action_detail_3 % 100,
                )
            elif self.action.action_detail_1 == 599:
                # skill_action_sp_if_dot_not
                false_clause = StringResources.get(
                    "skill_action_sp_if_dot_not",
                    self.get_target(),
                    self.action.action_detail_3 % 100,
                )
            elif (600 <= self.action.action_detail_1 <= 699) or (
                6000 <= self.action.action_detail_1 <= 6999
            ):
                # skill_action_sp_if_mark_count_not
                cnt = max(int(self.action.action_value_3), 1)
                false_clause = StringResources.get(
                    "skill_action_sp_if_mark_count_not",
                    self.get_target(),
                    cnt,
                    self.action.action_detail_3 % 100,
                )
            elif self.action.action_detail_1 == 700:
                # skill_action_if_alone_not
                false_clause = StringResources.get(
                    "skill_action_if_alone_not",
                    self.get_target(),
                    self.action.action_detail_3 % 100,
                )
            elif 701 <= self.action.action_detail_1 <= 709:
                # skill_action_sp_if_unit_count_not
                false_clause = StringResources.get(
                    "skill_action_sp_if_unit_count_not",
                    self.get_target(),
                    self.action.action_detail_1 - 700,
                    self.action.action_detail_3 % 100,
                )
            elif self.action.action_detail_1 == 720:
                # skill_action_sp_if_unit_exist_not
                false_clause = StringResources.get(
                    "skill_action_sp_if_unit_exist_not",
                    self.get_target(),
                    self.action.action_detail_3 % 100,
                )
            elif 901 <= self.action.action_detail_1 <= 999:
                # skill_action_if_hp_above
                false_clause = StringResources.get(
                    "skill_action_if_hp_above",
                    self.get_target(),
                    self.action.action_detail_1 - 900,
                    self.action.action_detail_3 % 100,
                )
            elif self.action.action_detail_1 == 1000:
                # skill_action_sp_if_kill_not
                false_clause = StringResources.get(
                    "skill_action_sp_if_kill_not", self.action.action_detail_3 % 100
                )
            elif self.action.action_detail_1 == 1001:
                # skill_action_sp_if_critical_not
                false_clause = StringResources.get(
                    "skill_action_sp_if_critical_not", self.action.action_detail_3 % 100
                )
            elif 1200 <= self.action.action_detail_1 <= 1299:
                # skill_action_sp_if_skill_count_not
                false_clause = StringResources.get(
                    "skill_action_sp_if_skill_count_not",
                    self.get_target(),
                    self.action.action_detail_1 % 10,
                    self.action.action_detail_3 % 100,
                )
            elif (
                self.action.action_detail_1 == 2000
                or self.action.action_detail_1 == 1300
            ):
                # skill_action_if_unit_atk_type ... magic
                false_clause = StringResources.get(
                    "skill_action_if_unit_atk_type",
                    self.get_target(),
                    StringResources.get("skill_status_magic_atk"),
                    self.action.action_detail_3 % 100,
                )
            elif self.action.action_detail_1 == 2001:
                # skill_action_if_unit_atk_type ... physical
                false_clause = StringResources.get(
                    "skill_action_if_unit_atk_type",
                    self.get_target(),
                    StringResources.get("skill_status_physical_atk"),
                    self.action.action_detail_3 % 100,
                )
            else:
                # skill_action_if_status_not
                false_clause = StringResources.get(
                    "skill_action_if_status_not",
                    self.get_target(),
                    status,
                    self.action.action_detail_3 % 100,
                )

        # 最后根据 trueClause 和 falseClause 的情况，组合返回值
        if true_clause != "UNKNOWN" and false_clause != "UNKNOWN":
            # "trueClause；falseClause"
            return StringResources.get(
                "skill_action_condition", f"{true_clause}；{false_clause}"
            )
        elif true_clause != "UNKNOWN":
            return StringResources.get("skill_action_condition", true_clause)
        elif false_clause != "UNKNOWN":
            return StringResources.get("skill_action_condition", false_clause)
        else:
            return "UNKNOWN"

    def coefficient(self, level: float = 1.0) -> str:
        """
        对应原 Kotlin fun SkillActionDetail.coefficient(): String 逻辑。
        """

        # ------------ 1) 计算 attrType ------------
        attr_type_map = {
            7: StringResources.get("skill_physical_str"),
            8: StringResources.get("skill_magic_str"),
            9: StringResources.get("skill_physical_def"),
            10: StringResources.get("skill_magic_def"),
        }
        attr_type = attr_type_map.get(self.action.action_value_1, "UNKNOWN")

        # ------------ 2) 计算 changeType ------------
        # SkillActionType.getByType(actionType) => get_by_type(actionType)
        sat = self.action.action_type
        if sat == SkillActionType.ADDITIVE.value:
            change_type = StringResources.get("skill_action_type_desc_additive")
        elif sat == SkillActionType.MULTIPLE.value:
            change_type = StringResources.get("skill_action_type_desc_multiple")
        elif sat == SkillActionType.DIVIDE.value:
            change_type = StringResources.get("skill_action_type_desc_divide")
        else:
            change_type = "UNKNOWN"

        # ------------ 3) 构造 commonDesc 字符串 ------------
        value = self.get_value_text(
            2, self.action.action_value_2, self.action.action_value_3, hide_index=True
        )
        common_desc = StringResources.get(
            "skill_action_change_coe",
            self.action.action_detail_1 % 100,
            self.action.action_detail_2,
            change_type,
            value,
        )

        # ------------ 4) 根据 self.action.action_value_1 不同取 extraDesc ------------
        av1 = int(self.action.action_value_1)
        extra_desc = "UNKNOWN"

        if av1 == 2:
            if self.action.action_detail_3 == 0:
                mValue = f"[{self.action.action_value_2}]"
            elif self.action.action_detail_2 == 0:
                mValue = f"[{self.action.action_value_3}]"
            else:
                mValue = f"[{self.action.action_value_2 + 2 * self.action.action_value_3 * level}] <{self.action.action_value_2} + {2 * self.action.action_value_3} * 技能等级> "

            m_desc = StringResources.get(
                "skill_action_change_coe",
                self.action.action_detail_1 % 100,
                self.action.action_detail_2,
                change_type,
                mValue,
            )
            extra_desc = StringResources.get("skill_action_change_coe_2", m_desc)

        elif av1 == 0:
            extra_desc = StringResources.get("skill_action_change_coe_0", common_desc)

        elif av1 == 1:
            extra_desc = StringResources.get("skill_action_change_coe_1", common_desc)

        elif av1 == 4:
            target_str = self.get_target()
            if target_str:
                target_type = target_str
            else:
                target_type = StringResources.get("skill_target_none")

            extra_desc = StringResources.get(
                "skill_action_change_coe_4", common_desc, target_type
            )

        elif av1 == 5:
            extra_desc = StringResources.get("skill_action_change_coe_5", common_desc)

        elif av1 == 6:
            extra_desc = StringResources.get("skill_action_change_coe_6", common_desc)

        elif 7 <= av1 <= 10:
            # getString(R.string.skill_action_change_coe_7_10, commonDesc, getTarget(), attrType)
            extra_desc = StringResources.get(
                "skill_action_change_coe_7_10",
                common_desc,
                self.get_target(),
                attr_type,
            )

        elif av1 == 12:
            extra_desc = StringResources.get(
                "skill_action_change_coe_12", common_desc, self.get_target()
            )

        elif av1 == 13:
            extra_desc = StringResources.get("skill_action_change_coe_13", common_desc)
        elif av1 == 15:
            extra_desc = StringResources.get(
                "skill_action_change_coe_15", common_desc, self.get_target()
            )
        elif av1 == 16:
            extra_desc = StringResources.get(
                "skill_action_change_coe_16", common_desc, self.get_target()
            )
        elif av1 == 102:
            extra_desc = StringResources.get("skill_action_change_coe_102", common_desc)
        elif 20 <= av1 < 30:
            extra_desc = StringResources.get(
                "skill_action_change_coe_skill_count", common_desc
            )
        elif (200 <= av1 < 300) or (2112 <= av1 < 3000):
            extra_desc = StringResources.get(
                "skill_action_change_coe_mark_count", common_desc
            )

        if int(self.action.action_value_4) == 0:
            return extra_desc
        # val limitValue = getValueText(4, actionValue4, actionValue5, hideIndex = true)
        limit_value = self.get_value_text(
            4,
            self.action.action_value_4,
            self.action.action_value_5,
            hide_index=True,
        )
        limit_desc = StringResources.get("skill_action_limit", limit_value)
        # extraDesc + limit
        return "UNKNOWN" if extra_desc == "UNKNOWN" else extra_desc + limit_desc

    # 24：复活
    def revival(self):
        return StringResources.get(
            "skill_action_type_desc_24",
            self.get_target(),
            int(self.action.action_value_2 * 100),
        )

    # 23：判定对象状态
    def if_status(self) -> str:
        status = get_status(self.action.action_detail_1, self.action.action_value_3)
        true_clause = "UNKNOWN"
        false_clause = "UNKNOWN"

        # ---------- 设置 true_clause ----------
        if self.action.action_detail_2 != 0:
            if status != StringResources.get("UNKNOWN"):
                # 原代码: getString(R.string.skill_action_if_status, getTarget(), status, self.action.action_detail_2 % 100)
                true_clause = StringResources.get(
                    "skill_action_if_status",
                    self.get_target(),
                    status,
                    self.action.action_detail_2 % 100,
                )
            else:
                # 根据 self.action.action_detail_1 不同范围进行判断
                if (
                    600 <= self.action.action_detail_1 <= 699
                    or self.action.action_detail_1 in [710, 6145]
                ):
                    # getString(R.string.skill_action_if_mark, getTarget(), self.action.action_detail_2 % 100)
                    true_clause = StringResources.get(
                        "skill_action_if_mark",
                        self.get_target(),
                        self.action.action_detail_2 % 100,
                    )
                elif self.action.action_detail_1 == 6194:
                    # getString(R.string.skill_action_if_mark_count, getTarget(), self.action.action_value_3.toInt(), self.action.action_detail_2 % 100)
                    true_clause = StringResources.get(
                        "skill_action_if_mark_count",
                        self.get_target(),
                        int(self.action.action_value_3),
                        self.action.action_detail_2 % 100,
                    )
                elif self.action.action_detail_1 == 700:
                    # getString(R.string.skill_action_if_alone, getTarget(), self.action.action_detail_2 % 100)
                    true_clause = StringResources.get(
                        "skill_action_if_alone",
                        self.get_target(),
                        self.action.action_detail_2 % 100,
                    )
                elif 901 <= self.action.action_detail_1 <= 999:
                    # getString(R.string.skill_action_if_hp_below, getTarget(), self.action.action_detail_1 - 900, self.action.action_detail_2 % 100)
                    true_clause = StringResources.get(
                        "skill_action_if_hp_below",
                        self.get_target(),
                        self.action.action_detail_1 - 900,
                        self.action.action_detail_2 % 100,
                    )
                elif self.action.action_detail_1 in [2000, 1300]:
                    # getString(R.string.skill_action_if_unit_atk_type, getTarget(), getString(R.string.skill_status_physical_atk), self.action.action_detail_2 % 100)
                    # 这里模拟 getString(R.string.skill_status_physical_atk) => "physical_atk"
                    true_clause = StringResources.get(
                        "skill_action_if_unit_atk_type",
                        self.get_target(),
                        "physical_atk",
                        self.action.action_detail_2 % 100,
                    )
                elif self.action.action_detail_1 == 2001:
                    # getString(R.string.skill_action_if_unit_atk_type, getTarget(), getString(R.string.skill_status_magic_atk), self.action.action_detail_2 % 100)
                    true_clause = StringResources.get(
                        "skill_action_if_unit_atk_type",
                        self.get_target(),
                        "magic_atk",
                        self.action.action_detail_2 % 100,
                    )
                else:
                    true_clause = "UNKNOWN"

        # ---------- 设置 false_clause ----------
        if self.action.action_detail_3 != 0:
            if status != StringResources.get("UNKNOWN"):
                # getString(R.string.skill_action_if_status_not, getTarget(), status, self.action.action_detail_3 % 100)
                false_clause = StringResources.get(
                    "skill_action_if_status_not",
                    self.get_target(),
                    status,
                    self.action.action_detail_3 % 100,
                )
            else:
                if (
                    600 <= self.action.action_detail_1 <= 699
                    or self.action.action_detail_1 in [710, 6145]
                ):
                    # getString(R.string.skill_action_if_mark_not, getTarget(), self.action.action_detail_3 % 100)
                    false_clause = StringResources.get(
                        "skill_action_if_mark_not",
                        self.get_target(),
                        self.action.action_detail_3 % 100,
                    )
                elif self.action.action_detail_1 == 6194:
                    # getString(R.string.skill_action_if_mark_count_not, getTarget(), self.action.action_value_3.toInt(), self.action.action_detail_3 % 100)
                    false_clause = StringResources.get(
                        "skill_action_if_mark_count_not",
                        self.get_target(),
                        int(self.action.action_value_3),
                        self.action.action_detail_3 % 100,
                    )
                elif self.action.action_detail_1 == 700:
                    # getString(R.string.skill_action_if_alone_not, getTarget(), self.action.action_detail_3 % 100)
                    false_clause = StringResources.get(
                        "skill_action_if_alone_not",
                        self.get_target(),
                        self.action.action_detail_3 % 100,
                    )
                elif 901 <= self.action.action_detail_1 <= 999:
                    # getString(R.string.skill_action_if_hp_above, getTarget(), self.action.action_detail_1 - 900, self.action.action_detail_3 % 100)
                    false_clause = StringResources.get(
                        "skill_action_if_hp_above",
                        self.get_target(),
                        self.action.action_detail_1 - 900,
                        self.action.action_detail_3 % 100,
                    )
                elif self.action.action_detail_1 in [2000, 1300]:
                    # 原代码中的“else分支”与 truth 分支相反；对 atk_type 逻辑做相反处理
                    false_clause = StringResources.get(
                        "skill_action_if_unit_atk_type",
                        self.get_target(),
                        StringResources.get("skill_status_magic_atk"),
                        self.action.action_detail_3 % 100,
                    )
                elif self.action.action_detail_1 == 2001:
                    false_clause = StringResources.get(
                        "skill_action_if_unit_atk_type",
                        self.get_target(),
                        StringResources.get("skill_status_physical_atk"),
                        self.action.action_detail_3 % 100,
                    )
                else:
                    false_clause = "UNKNOWN"
        # ---------- 最终返回结果 ----------
        # 原 Kotlin: if (self.action.action_detail_1 in 0..99) { ... } else { ... }
        if 0 <= self.action.action_detail_1 <= 99:
            # 满足 0..99 时，走 “随机” 分支
            if self.action.action_detail_2 != 0 and self.action.action_detail_3 != 0:
                # getString(R.string.skill_action_random_1, self.action.action_detail_1, self.action.action_detail_2 % 100, self.action.action_detail_3 % 100)
                return StringResources.get(
                    "skill_action_random_1",
                    self.action.action_detail_1,
                    self.action.action_detail_2 % 100,
                    self.action.action_detail_3 % 100,
                )
            elif self.action.action_detail_2 != 0:
                # getString(R.string.skill_action_random_2, self.action.action_detail_1, self.action.action_detail_2 % 100)
                return StringResources.get(
                    "skill_action_random_2",
                    self.action.action_detail_1,
                    self.action.action_detail_2 % 100,
                )
            elif self.action.action_detail_3 != 0:
                # getString(R.string.skill_action_random_2, 100 - self.action.action_detail_1, self.action.action_detail_3 % 100)
                return StringResources.get(
                    "skill_action_random_2",
                    100 - self.action.action_detail_1,
                    self.action.action_detail_3 % 100,
                )
            else:
                return "UNKNOWN"
        elif true_clause != "UNKNOWN" and false_clause != "UNKNOWN":
            # getString(R.string.skill_action_condition, "${trueClause}；${falseClause}")
            # 注意原 Kotlin 用的是 “；” 分隔，这里也用同样符号
            return StringResources.get(
                "skill_action_condition", f"{true_clause}；{false_clause}"
            )
        elif true_clause != "UNKNOWN":
            # getString(R.string.skill_action_condition, trueClause)
            return StringResources.get("skill_action_condition", true_clause)
        elif false_clause != "UNKNOWN":
            # getString(R.string.skill_action_condition, falseClause)
            return StringResources.get("skill_action_condition", false_clause)
        else:
            return "UNKNOWN"

    # 22：循环变更
    def change_pattern(self):
        if self.action.action_detail_1 == 1:
            return StringResources.get(
                "skill_action_loop_change",
                (
                    self.get_time_text(1, self.action.action_value_1)
                    if self.action.action_value_1 > 0
                    else ""
                ),
            )
        elif self.action.action_detail_1 == 2:
            return StringResources.get(
                "skill_action_skill_anim_change",
                self.get_time_text(1, self.action.action_value_1),
            )
        else:
            return "UNKNOWN"

    # 21：回避
    def invincible(self):
        # 回避等技能限制
        init_other_limit()
        self.tag = StringResources.get(
            {
                1: "skill_action_type_desc_21_1",
                2: "skill_action_type_desc_21_2",
                3: "skill_action_type_desc_21_3",
                6: "skill_action_type_desc_21_6",
                8: "skill_action_type_desc_21_8",
            }.get(self.action.action_detail_1, "unknown")
        )

        if self.action.action_value_1 <= 0:
            return self.tag
        time = self.get_time_text(
            1, self.action.action_value_1, self.action.action_value_2
        )
        return f"{self.tag}{time}"

    # 20：挑衅
    def taunt(self):
        # 回避等技能限制
        init_other_limit()
        time = self.get_time_text(
            1, self.action.action_value_1, self.action.action_value_2
        )
        return StringResources.get(
            "skill_action_type_desc_20",
            self.get_target(),
            self.action.ailment_name,
            time,
        )

    # 93：无视挑衅
    def ignore_taunt(self):
        return StringResources.get("skill_action_type_desc_93", self.get_target())

    # 18：蓄力、19：伤害充能
    def charge(self):
        desc = StringResources.get(
            "skill_action_type_desc_18_19", str(self.action.action_value_3)
        )

        if self != 0.0 or self.action.action_value_2 != 0.0:
            value = self.get_value_text(
                1, self.action.action_value_1, self.action.action_value_2
            )
            extra_desc = StringResources.get(
                "skill_action_type_desc_18_19_detail",
                self.action.action_detail_2 % 100,
                value,
            )
        else:
            extra_desc = ""

        return desc + extra_desc

    # 17：触发条件
    def trigger(self):
        desc = {
            2: StringResources.get(
                "skill_action_type_desc_17_2", self.action.action_value_1
            ),
            3: StringResources.get(
                "skill_action_type_desc_17_3", self.action.action_value_3
            ),
            4: StringResources.get(
                "skill_action_type_desc_17_4", self.action.action_value_1
            ),
            5: StringResources.get(
                "skill_action_type_desc_17_5", self.action.action_value_1
            ),
            7: StringResources.get(
                "skill_action_type_desc_17_7", self.action.action_value_3
            ),
            8: StringResources.get(
                "skill_action_type_desc_17_8", self.action.action_value_1
            ),
            9: StringResources.get(
                "skill_action_type_desc_17_9",
                self.action.action_value_1,
                self.get_time_text(3, self.action.action_value_3),
            ),
            10: StringResources.get(
                "skill_action_type_desc_17_10", self.action.action_value_1
            ),
            11: StringResources.get("skill_action_type_desc_17_11"),
            13: StringResources.get(
                "skill_action_type_desc_17_13", self.action.action_value_3
            ),
            14: StringResources.get(
                "skill_action_type_desc_17_17", self.action.action_value_1
            ),
        }.get(self.action.action_detail_1, "UNKNOWN")

        return StringResources.get("skill_action_condition", desc)

    # 42：触发
    def loop_trigger(self):
        if self.action.action_detail_1 == 2:
            value = self.get_value_text(
                1,
                self.action.action_value_1,
                self.action.action_value_2,
                0.0,
                percent="%",
            )
            return StringResources.get(
                "skill_action_type_desc_42_2",
                self.action.action_value_4,
                value,
                self.action.action_detail_2 % 100,
            )
        elif self.action.action_detail_1 == 14:
            value = self.get_value_text(
                1,
                self.action.action_value_1,
                self.action.action_value_2,
                0.0,
                percent="%",
            )
            action_text = StringResources.get(
                "skill_action_d", self.action.action_detail_2 % 100
            )
            if self.action.action_detail_3 != 0:
                action_text += "、" + StringResources.get(
                    "skill_action_d", self.action.action_detail_3 % 100
                )
            return StringResources.get(
                "skill_action_type_desc_42_14",
                self.action.action_value_4,
                value,
                action_text,
            )
        else:
            return "UNKNOWN"

    # 111：触发条件？
    def trigger_v2(self):
        effect_map = {
            1: StringResources.get("skill_action_type_desc_77_1")
            + StringResources.get("skill_buff"),
            2: StringResources.get("skill_action_type_desc_77_1")
            + StringResources.get("skill_action_type_desc_111_2"),
        }
        effect = effect_map.get(self.action.action_detail_1, "UNKNOWN")
        return StringResources.get(
            "skill_action_type_desc_111",
            self.get_target(),
            effect,
            self.action.action_detail_2 % 100,
        )

    # 16：TP 相关
    def tp(self):
        value = self.get_value_text(
            1, self.action.action_value_1, self.action.action_value_2
        )
        self.tag = StringResources.get(
            "skill_action_tp_recovery"
            if self.action.action_detail_1 in [1, 4]
            else "skill_action_tp_reduce"
        )
        return f"{self.get_target()}{self.tag} {value}"

    # 92：改变 TP 获取倍率
    def change_tp_ratio(self):
        return StringResources.get(
            "skill_action_type_desc_92",
            self.get_target(),
            str(self.action.action_value_1),
        )

    # 97：受击tp回复
    def tp_hit(self):
        limit = StringResources.get(
            "skill_action_limit_int", self.action.action_value_4
        )
        time = self.get_time_text(5, self.action.action_value_5)
        desc = StringResources.get(
            "skill_action_type_desc_35",
            self.get_target(),
            self.action.action_value_3,
            time,
            limit,
        )
        tp_desc = StringResources.get(
            "skill_action_type_desc_97", self.action.action_value_1
        )
        return desc + tp_desc

    # 98：改变 TP 减少时倍率
    def tp_hit_reduce(self):
        time = self.get_time_text(
            2, self.action.action_value_2, self.action.action_value_3
        )
        return StringResources.get(
            "skill_action_type_desc_98",
            self.get_target(),
            str(self.action.action_value_1),
            time,
        )

    # 15：召唤
    def summon(self):
        desc = StringResources.get("skill_action_summon_unit")
        if self.action.action_value_7 > 0:
            return StringResources.get(
                "skill_action_type_desc_15",
                self.get_target(),
                StringResources.get("skill_ahead"),
                self.action.action_value_7,
                desc,
            )
        elif self.action.action_value_7 < 0:
            return StringResources.get(
                "skill_action_type_desc_15",
                self.get_target(),
                StringResources.get("skill_rear"),
                abs(self.action.action_value_7),
                desc,
            )
        else:
            return StringResources.get(
                "skill_action_summon_target", self.get_target(), desc
            )

    def change_mode(self):
        return {
            1: StringResources.get(
                "skill_action_change_mode",
                (
                    StringResources.get("skill_action_change_to_flight_status")
                    if self.action.action_value_5 == 1
                    else StringResources.get("none")
                ),
                self.get_time_text(1, self.action.action_value_1),
            ),
            2: StringResources.get(
                "skill_action_type_desc_14_2", self.action.action_value_1
            ),
            3: StringResources.get("skill_action_type_desc_14_3"),
        }.get(self.action.action_detail_1, "UNKNOWN")

    # 11：魅惑/混乱12：黑暗 13：沉默
    def charm(self):
        chance = self.get_value_text(
            3,
            self.action.action_value_3,
            (
                0.0
                if int(
                    self.action.action_value_3,
                )
                == 100
                else 1.0
            ),
            0.0,
            percent="%",
        )
        time = self.get_time_text(
            1, self.action.action_value_1, self.action.action_value_2
        )

        if self.action.action_type == SkillActionType.CHARM.value:
            self.tag = StringResources.get(
                {0: "skill_charm_0", 1: "skill_charm_1"}.get(
                    self.action.action_detail_1, "unknown"
                )
            )
        elif self.action.action_type == SkillActionType.SILENCE.value:
            self.tag = StringResources.get("SKILL_TYPE_13")

        result = StringResources.get(
            "skill_action_type_desc_12_13", chance, self.get_target(), self.tag, time
        )

        if self.action.action_type == SkillActionType.BLIND.value:
            result += StringResources.get(
                "skill_action_atk_miss", 100 - self.action.action_detail_1
            )

        return result

    # 10：buff/debuff
    def aura(self):
        self.tag = StringResources.get(
            "skill_buff" if self.action.action_detail_1 % 10 == 0 else "skill_debuff"
        )

        if self.action.action_detail_1 % 1000 // 10 == 5:
            # 回避等技能限制
            init_other_limit()

        value = self.get_value_text(
            2,
            self.action.action_value_2,
            self.action.action_value_3,
            percent=self.get_percent(),
        )
        aura = get_aura(self.action.action_detail_1, value)
        time = self.get_time_text(
            4, self.action.action_value_4, self.action.action_value_5
        )

        if self.action.action_detail_2 == 2:
            return StringResources.get(
                "skill_action_type_desc_10_break", self.get_target(), aura
            )
        else:
            return f"{self.get_target()}{aura}{time}"

    def dot(self):
        self.tag = StringResources.get(
            {
                0: "skill_dot_0",
                1: "skill_dot_1_7",
                7: "skill_dot_1_7",
                2: "skill_dot_2",
                3: "skill_dot_3_8",
                8: "skill_dot_3_8",
                4: "skill_dot_4",
                5: "skill_dot_5",
                11: "skill_dot_11",
            }.get(self.action.action_detail_1, "unknown")
        )

        value = self.get_value_text(
            1,
            self.action.action_value_1,
            self.action.action_value_2,
            percent=self.get_percent(),
        )
        time = self.get_time_text(
            3, self.action.action_value_3, self.action.action_value_4
        )
        dot_increase = (
            StringResources.get("skill_action_dot_increase", self.action.action_value_5)
            if self.action.action_detail_1 == 5
            else ""
        )

        return StringResources.get(
            "skill_action_type_desc_9",
            self.get_target(),
            self.tag,
            value,
            dot_increase,
            time,
        )

    # 110：持续伤害易伤
    def dot_up(self):
        value = self.get_value_text(
            1, self.action.action_value_1, self.action.action_value_2
        )
        limit = StringResources.get(
            "skill_action_damage_limit_int", self.action.action_value_7
        )
        return StringResources.get(
            "skill_action_type_desc_110", self.get_target(), value, limit
        )

    # 79：行动时，造成伤害
    def action_dot(self):
        value = self.get_value_text(
            1,
            self.action.action_value_1,
            self.action.action_value_2,
            percent=self.get_percent(),
        )
        time = self.get_time_text(
            3, self.action.action_value_3, self.action.action_value_4
        )
        if self.action.action_detail_1 == 10:
            type_ = StringResources.get("skill_hp_max")
            limit = StringResources.get(
                "skill_action_damage_limit_int", self.action.action_value_5
            )
        else:
            type_ = ""
            limit = ""

        return StringResources.get(
            "skill_action_type_desc_79", self.get_target(), type_, value, time, limit
        )

    # 8：行动速度变更、83：可叠加行动速度变更、99：范围速度变更
    def speed(self):
        # 判断异常状态
        self.tag = StringResources.get(
            {
                1: "skill_ailment_1",
                2: "skill_ailment_2",
                3: "skill_ailment_3",
                4: "skill_ailment_4",
                5: "skill_ailment_5",
                6: "skill_ailment_6",
                7: "skill_ailment_7_12_14",
                12: "skill_ailment_7_12_14",
                14: "skill_ailment_7_12_14",
                8: "skill_ailment_8",
                9: "skill_ailment_9",
                10: "skill_ailment_10",
                11: "skill_ailment_11",
                13: "skill_ailment_13",
            }.get(self.action.action_detail_1, "unknown")
        )

        value = self.get_value_text(
            1, self.action.action_value_1, self.action.action_value_2
        )
        time = self.get_time_text(
            3, self.action.action_value_3, self.action.action_value_4
        )

        # 额外、范围速度变更
        if (
            self.action.action_type
            == SkillActionType.SUPERIMPOSE_CHANGE_ACTION_SPEED.value
        ):
            self.tag += StringResources.get("skill_ailment_extra")
        elif self.action.action_type == "SPEED_FIELD":
            self.tag += StringResources.get("skill_ailment_field")

        if self.action.action_detail_1 in [1, 2]:
            if (
                self.action.action_type
                == SkillActionType.SUPERIMPOSE_CHANGE_ACTION_SPEED.value
            ):
                type_ = StringResources.get(
                    "skill_reduce"
                    if self.action.action_detail_1 == 1
                    else "skill_increase"
                )
                desc_text = StringResources.get(
                    "skill_action_speed_change", type_, value
                )
            else:
                desc_text = StringResources.get("skill_action_speed_multiple", value)

            if self.action.action_type == SkillActionType.SPEED_FIELD:
                return StringResources.get(
                    "skill_action_type_desc_field",
                    self.action.action_value_5,
                    desc_text,
                    time,
                )
            else:
                return f"{self.tag}{self.get_target()}，{desc_text}{time}"
        else:
            count = (
                StringResources.get("skill_action_hit_remove")
                if self.action.action_detail_2 == 1
                else ""
            )
            return StringResources.get(
                "skill_action_type_desc_8", self.get_target(), self.tag, time, count
            )

    # 100：免疫无法行动的异常状态
    def ignore_speed_down(self):
        time = self.get_time_text(3, self.action.action_value_3)
        limit = (
            StringResources.get("none")
            if self.action.action_value_1 == -1
            else StringResources.get(
                "skill_action_type_desc_100_count", self.action.action_value_1
            )
        )
        return StringResources.get(
            "skill_action_type_desc_100", self.get_target(), limit, time
        )

    def choose_enemy(self):
        return StringResources.get("skill_action_type_desc_7", self.get_target())

    # 6：护盾
    def barrier(self):
        value = self.get_value_text(
            1, self.action.action_value_1, self.action.action_value_2
        )
        time = self.get_time_text(
            3, self.action.action_value_3, self.action.action_value_4
        )
        type_ = get_barrier_type(self.action.action_detail_1)
        if type_ != "UNKNOWN":
            return StringResources.get(
                "skill_action_type_desc_6", self.get_target(), type_, value, time
            )
        else:
            return type_

    # 73：伤害护盾
    def log_barrier(self):
        time = self.get_time_text(
            3, self.action.action_value_3, self.action.action_value_4
        )
        return StringResources.get(
            "skill_action_type_desc_73",
            self.get_target(),
            self.action.action_value_5,
            time,
        )

    def heal(self):
        value = self.get_value_text(
            2,
            self.action.action_value_2,
            self.action.action_value_3,
            self.action.action_value_4,
        )
        return StringResources.get("skill_action_type_desc_4", self.get_target(), value)

    # 59：回复妨碍
    def inhibit_heal(self):
        return StringResources.get(
            "skill_action_type_desc_59",
            self.get_target(),
            int(self.action.action_value_1 * 100),
            self.get_time_text(2, self.action.action_value_2),
        )

    # 76：HP 回复量变化
    def heal_down(self):
        value = self.get_value_text(
            1,
            self.action.action_value_1,
            self.action.action_value_2,
            percent=self.get_percent(),
        )
        time = self.get_time_text(
            3, self.action.action_value_3, self.action.action_value_4
        )
        return StringResources.get(
            "skill_action_type_desc_76", self.get_target(), value, time
        )

    def change_position(self):
        if self.action.action_detail_1 in [1, 9]:
            return StringResources.get(
                "skill_action_type_desc_3_up",
                StringResources.get("skill_hit_up"),
                self.get_target(),
                abs(self.action.action_value_1),
            )
        elif self.action.action_detail_1 in [3, 6]:
            return StringResources.get(
                "skill_action_type_desc_3_move",
                StringResources.get(
                    "skill_push" if self.action.action_value_1 > 0 else "skill_pull"
                ),
                self.get_target(),
                abs(self.action.action_value_1),
            )
        elif self.action.action_detail_1 == 8:
            return StringResources.get(
                "skill_action_type_desc_3_pull",
                self.get_target(),
                StringResources.get("skill_pull"),
                self.action.action_value_1,
            )
        else:
            return "UNKNOWN"

    def move(self):
        direction_text = (
            StringResources.get("skill_forward")
            if self.action.action_value_1 > 0
            else StringResources.get("skill_backward")
        )
        position_text = (
            StringResources.get("skill_ahead")
            if self.action.action_value_1 > 0
            else StringResources.get("skill_rear")
        )

        move_text = StringResources.get(
            "skill_move",
            self.get_target(),
            position_text,
            abs(self.action.action_value_1),
        )
        return_text = StringResources.get("skill_return")
        speed_text = StringResources.get("skill_move_speed", self.action.action_value_2)

        return {
            1: move_text + return_text,
            2: direction_text + move_text + return_text,
            3: move_text,
            4: direction_text + move_text,
            5: move_text + speed_text,
            6: direction_text + move_text + speed_text,
            7: direction_text + move_text,
        }.get(self.action.action_detail_1, "UNKNOWN")

    def damage(self):
        atk_type = get_atk_type(self.action.action_detail_1)
        adaptive = (
            "(适应物理/魔法防御中较低的防御)"
            if self.action.action_detail_2 == 1
            else ""
        )

        # 暴伤倍率
        multiple_damage = ""
        if self.action.action_value_6 > 0:
            if self.action.action_value_6 > 1:
                multiple = f"[{self.action.action_value_6 * 2}]"
            else:
                multiple = "[2]"
            multiple_damage = f"暴击时，造成 {multiple} 倍伤害"

        # 必定暴击
        must_critical = "必定暴击" if self.action.action_value_5 == 1 else ""

        # 无视防御，fixme 需优化逻辑，龙拳为0但需要显示，106501108 106501109
        ignore_def = (
            f"无视目标 [{self.action.action_value_7}] 防御力"
            if self.action.action_value_7 > 0
            or self.action.action_id in [106501108, 106501109]
            else ""
        )

        value = self.get_value_text(
            1,
            self.action.action_value_1,
            self.action.action_value_2,
            self.action.action_value_3,
            v4=self.action.action_value_4,
        )

        return StringResources.get(
            "skill_action_type_desc_1",
            self.get_target(),
            value,
            atk_type,
            adaptive,
            multiple_damage,
            must_critical,
            ignore_def,
        )

    # 125：无法选中
    def cannot_selected(self):
        status = StringResources.get("skill_action_type_125")
        return StringResources.get(
            "skill_action_type_desc_125", self.get_target(), status
        )

    def buff_dot(self):
        return StringResources.get(
            "skill_action_type_desc_128",
            self.get_target(),
            self.action.action_value_1 // 100,
            self.get_time_text(2, self.action.action_value_2),
        )

    def damage2dot(self):
        return StringResources.get(
            "skill_action_type_desc_129",
            self.get_target(),
            self.get_value_text(1, v1=self.action.action_value_1, v2=0.0, percent="%"),
            self.get_time_text(2, self.action.action_value_2),
        )

    def change_def_max(self):
        return StringResources.get(
            "skill_action_type_desc_130",
            self.get_target(),
        )

    def get_value_text(
        self,
        index,
        v1,
        v2,
        v3=0.0,
        v4=0.0,
        percent="",
        hide_index=False,
        max_value=None,
    ):
        skill_level_text = StringResources.get("skill_level_text")
        skill_atk_str_text = StringResources.get("skill_atk_text")
        if v3 == 0.0:
            if v1 == 0.0 and v2 != 0.0:
                value = f"[{int(v2 * self.level)}{percent}] <{{{index + 1}}}{v2} * {skill_level_text}>"
            elif v1 != 0.0 and v2 == 0.0:
                value = f"{{{index}}}[{v1}{percent}]"
            elif v1 != 0.0:
                value = f"[{int(v1 + v2 * self.level)}{percent}] <{{{index}}}{v1} + {{{index + 1}}}{v2} * {skill_level_text}>"
            else:
                value = f"{{{index}}}[0]{percent}"
        elif v4 != 0.0:
            value = f"[{int(v1 + v2 * self.level + (v3 + v4 * self.level) * self.atk)}{percent}] <{{{index}}}{v1} + {{{index + 1}}}{v2} * {skill_level_text} + ﹙{{{index + 2}}}{v3} + {{{index + 3}}}{v4} * {skill_level_text}﹚ * {skill_atk_str_text}>"
        elif v1 == 0.0 and v2 != 0.0:
            value = f"[{int(v2 + v3 * self.atk)}{percent}] <{{{index + 1}}}{v2} + {{{index + 2}}}{v3} * {skill_atk_str_text}>"
        elif v1 == 0.0:
            value = f"[{int(v3 * self.atk)}{percent}] <{{{index + 2}}}{v3} * {skill_atk_str_text}>"
        elif v2 != 0.0:
            value = f"[{int(v1 + v2 * self.level + v3 * self.atk)}{percent}] <{{{index}}}{v1} + {{{index + 1}}}{v2} * {skill_level_text} + {{{index + 2}}}{v3} * {skill_atk_str_text}>"
        else:
            value = f"{{{index}}}[0]{percent}"

        if max_value is not None:
            value = re.sub(r"\[.*?\]", f"[{int(max_value)}{percent}]", value)

        if hide_index:
            value = re.sub(r"\{.*?\}", "", value)

        if not self.level:
            value = re.sub(r"\[.*?\] <", " <", value)

        return value

    def get_target_assignment(self):
        if self.action.target_type == 7:
            return StringResources.get("none")
        return StringResources.get(
            {
                0: "skill_target_assignment_0",
                1: "skill_target_assignment_1",
                2: "skill_target_assignment_2",
                3: "skill_target_assignment_3",
            }.get(self.action.target_assignment, "none")
        )

    def get_target_number(self):
        order = ""
        if self.action.target_assignment == 1:
            if 1 <= self.action.target_number <= 10:
                order = StringResources.get(
                    "skill_target_order_num", self.action.target_number + 1
                )
        elif self.action.target_number == 1:
            order = StringResources.get("skill_target_order_1")
        elif 1 < self.action.target_number <= 10:
            order = StringResources.get(
                "skill_target_order_num", self.action.target_number
            )

        return f"『{order}』" if order else ""

    def get_target_count(self):
        if self.action.target_count == 0:
            return ""
        elif self.action.target_count == 1:
            return (
                StringResources.get("skill_target_single")
                if self.action.target_assignment == 1
                else ""
            )
        elif self.action.target_count == 99:
            return StringResources.get("skill_target_all")
        else:
            return StringResources.get("skill_target_count", self.action.target_count)

    def get_target_range(self):
        return (
            f"『{StringResources.get('skill_range', self.action.target_range)}』"
            if 1 <= self.action.target_range < 2160
            else ""
        )

    def get_target(self):
        depend_dict = get_skill_depend_dict(self.skill_data)
        depend_id = depend_dict.get(self.action.action_id, 0)
        depend = (
            StringResources.get("skill_depend_action", depend_id % 100)
            if depend_id != 0
            else ""
        )
        if (
            self.action.target_count == 99
            and self.action.target_range == 2160
            and self.action.action_value_6 == 1
            and self.action.action_value_7 == 0
            and self.action.action_detail_2 == 1
        ):
            # fixme 敌方友方均生效，判断逻辑
            range_text = StringResources.get("skill_target_assignment_3")
        else:
            range_text = (
                self.get_target_number()
                + self.get_target_range()
                + self.get_target_assignment()
            )
        if target_type := self.get_target_type():
            target_type = f"『{target_type}』"

        return depend + target_type + range_text + self.get_target_count()

    def get_target_type(self) -> str:
        if self.action.target_type in [0, 1, 3, 40, 41]:
            return StringResources.get("none")
        elif self.action.target_type in [2, 8]:
            return StringResources.get("skill_target_2_8")
        elif self.action.target_type == 4:
            return StringResources.get("skill_target_4")
        elif self.action.target_type in [5, 25]:
            return StringResources.get("skill_target_5_25")
        elif self.action.target_type in [6, 26]:
            return StringResources.get("skill_target_6_26")
        elif self.action.target_type == 7:
            return StringResources.get("skill_target_7")
        elif self.action.target_type == 9:
            return StringResources.get("skill_target_9")
        elif self.action.target_type == 10:
            return StringResources.get("skill_target_10")
        elif self.action.target_type == 11:
            return StringResources.get("skill_target_11")
        elif self.action.target_type in [12, 27, 37]:
            return StringResources.get("skill_target_12_27_37")
        elif self.action.target_type in [13, 19, 28]:
            return StringResources.get("skill_target_13_19_28")
        elif self.action.target_type in [14, 29]:
            return StringResources.get("skill_target_14_29")
        elif self.action.target_type in [15, 30]:
            return StringResources.get("skill_target_15_30")
        elif self.action.target_type in [16, 31]:
            return StringResources.get("skill_target_16_31")
        elif self.action.target_type in [17, 32]:
            return StringResources.get("skill_target_17_32")
        elif self.action.target_type == 18:
            return StringResources.get("skill_target_18")
        elif self.action.target_type == 20:
            return StringResources.get("skill_target_20")
        elif self.action.target_type == 21:
            return StringResources.get("skill_target_21")
        elif self.action.target_type == 22:
            return StringResources.get("skill_target_22")
        elif self.action.target_type == 23:
            return StringResources.get("skill_target_23")
        elif self.action.target_type == 24:
            return StringResources.get("skill_target_24")
        elif self.action.target_type == 33:
            return StringResources.get("skill_target_33")
        elif self.action.target_type == 34:
            return StringResources.get("skill_target_34")
        elif self.action.target_type == 35:
            return StringResources.get("skill_target_35")
        elif self.action.target_type == 36:
            return StringResources.get("skill_target_36")
        elif self.action.target_type == 38:
            return StringResources.get("skill_target_38")
        elif self.action.target_type == 39:
            return StringResources.get("skill_target_39")
        elif self.action.target_type == 42:
            return StringResources.get("skill_target_42")
        elif self.action.target_type == 43:
            return StringResources.get("skill_target_43")
        elif self.action.target_type == 44:
            return StringResources.get("skill_target_44")
        elif self.action.target_type == 45:
            return StringResources.get("skill_target_45")
        elif self.action.target_type == 46:
            return StringResources.get("skill_target_46")
        elif self.action.target_type == 50:
            return StringResources.get("skill_target_50")
        elif 13195 <= self.action.target_type <= 14000:
            return StringResources.get("skill_target_13xxx")
        elif self.action.target_type in [14001, 15001]:
            return StringResources.get("skill_target_fire")
        elif self.action.target_type in [14002, 15002]:
            return StringResources.get("skill_target_water")
        elif self.action.target_type in [14003, 15003]:
            return StringResources.get("skill_target_wind")
        elif self.action.target_type in [14004, 15004]:
            return StringResources.get("skill_target_light")
        elif self.action.target_type in [15005, 14005]:
            return StringResources.get("skill_target_dark")
        else:
            return StringResources.get("unknown")

    def get_time_text(self, index, v1, v2=0.0, hide_index=False):
        return StringResources.get(
            "skill_effect_time",
            self.get_value_text(index, v1, v2, hide_index=hide_index),
        )

    def get_percent(self):
        if self.action.action_type in [
            SkillActionType.AURA.value,
            SkillActionType.HEAL_DOWN.value,
        ]:
            if self.action.action_value_1 == 2 or (
                self.action.action_detail_1 // 10
            ) in {
                11,
                12,
                14,
                16,
                17,
                18,
                19,
            }:
                return "%"
            else:
                return ""
        elif self.action.action_type in [
            SkillActionType.HEAL_FIELD.value,
            SkillActionType.AURA_FIELD.value,
        ]:
            return "%" if self.action.action_detail_2 == 2 else ""
        elif self.action.action_type == SkillActionType.DAMAGE_REDUCE.value:
            return "%"
        elif self.action.action_type == SkillActionType.ACTION_DOT.value:
            return "%" if self.action.action_detail_1 == 10 else ""
        elif self.action.action_type == SkillActionType.DOT.value:
            return "%" if self.action.action_detail_1 == 11 else ""
        else:
            return ""


action_handler = ActionHandler()
