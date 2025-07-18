from typing import Dict, List

from ..skill_text_handle import get_action_description, process_action_data

from ..model import SkillActionData
from .util import draw_text_with_base, get_text_size, merge_pic
from ..base import FilePath, Color
from ..table import UnitAttackPattern, SkillData, UnitSkillData
from ..util import is_text_chinese, split_list, split_text
from PIL import Image, ImageDraw, ImageFont
from ..download import get_skill_icon

WIDTH = 500
MARGIN = 30

TAG_PAIRS = {"<": ">", "[": "]", "『": "』", "{": "}"}
TAG_COLORS = {
    "<": "#a24072",
    "[": "#7aa57b",
    "『": "#a24072",
    "{": "#b476cd",
}


def pattern2skill_id(pattern_list: List[int], unit_skill: UnitSkillData) -> int:
    skill_list = []
    skill_type_list = []
    # 技能id
    main_skill_list = (
        unit_skill.main_skill_1,
        unit_skill.main_skill_2,
        unit_skill.main_skill_3,
        unit_skill.main_skill_4,
        unit_skill.main_skill_5,
        unit_skill.main_skill_6,
        unit_skill.main_skill_7,
        unit_skill.main_skill_8,
        unit_skill.main_skill_9,
        unit_skill.main_skill_10,
    )
    # sp技能id
    sp_skill_list = (
        unit_skill.sp_skill_1,
        unit_skill.sp_skill_2,
        unit_skill.sp_skill_3,
        unit_skill.sp_skill_4,
        unit_skill.sp_skill_5,
    )
    for pattern in pattern_list:
        if pattern in (1, 0):
            skill_list.append(1)
            skill_type_list.append("普攻")
        elif pattern // 1000 == 1:
            index = pattern % 100
            skill_list.append(main_skill_list[index - 1])
            skill_type_list.append(f"技能{index}")
        elif pattern // 1000 == 2:
            index = pattern % 100
            skill_list.append(sp_skill_list[index - 1])
            skill_type_list.append(f"SP技能{index}")
        else:
            raise ValueError(f"未知的技能id: {pattern}")
    return skill_list, skill_type_list


async def draw_pattern(
    attack_patterns: List[UnitAttackPattern],
    unit_skill: UnitSkillData,
    skill_data_dict: Dict[int, SkillData],
):
    pic_list = []
    if len(attack_patterns) == 1:
        return await draw_single_pattern(
            attack_patterns[0], unit_skill, skill_data_dict
        )
    for i, attack_pattern in enumerate(attack_patterns, start=1):
        pic = await draw_single_pattern(attack_pattern, unit_skill, skill_data_dict, i)
        pic_list.append(pic)
    return merge_pic(pic_list)


async def draw_single_pattern(
    attack_pattern: UnitAttackPattern,
    unit_skill: UnitSkillData,
    skill_data_dict: Dict[int, SkillData],
    num: int = 0,
):

    pattern_list = [
        _id
        for i in range(attack_pattern.loop_end)
        if (_id := getattr(attack_pattern, f"atk_pattern_{i+1}"))
    ]
    skill_list, skill_type_list = pattern2skill_id(pattern_list, unit_skill)
    pattern_list = split_list(skill_list)
    skill_type_list = split_list(skill_type_list)

    base = Image.new("RGBA", (WIDTH, 40 + 90 * len(pattern_list)), "#fef8f8")
    draw = ImageDraw.Draw(base)
    text_font_path = FilePath.font_ms_bold.value

    font = ImageFont.truetype(text_font_path, 15)

    height = 0
    text = f"技能模式{num}" if num else "技能模式"
    draw.text(
        (WIDTH // 2 - MARGIN * 2, height),
        text,
        "#a5366f",
        ImageFont.truetype(text_font_path, 25),
    )
    height += 50

    for j, (row1, row2) in enumerate(zip(pattern_list, skill_type_list)):
        for i, skill_id in enumerate(row1):
            icon_path = await get_skill_icon(
                1 if skill_id == 1 else skill_data_dict[skill_id].icon_type
            )
            icon = Image.open(icon_path).convert("RGBA").resize((50, 50))
            base.paste(icon, (MARGIN + i * 70, height + 90 * j))
            draw.text(
                (MARGIN + i * 70, height + 50 + 90 * j),
                row2[i],
                "#000000",
                font,
            )

    start_j, start_i = divmod(attack_pattern.loop_start - 1, 6)
    end_j, end_i = divmod(sum(len(pattern) for pattern in pattern_list) - 1, 6)

    draw.text(
        (MARGIN + start_i * 70, height - 20 + 90 * start_j),
        "循环开始",
        "#000000",
        font,
    )

    draw.text(
        (MARGIN + end_i * 70, height - 20 + 90 * end_j),
        "循环结束",
        "#000000",
        font,
    )

    return base


skill_type_color = {
    "连结爆发": Color.gold.value,
    "连结爆发+": Color.gold.value,
    "技能1": "#b476cd",
    "技能1+": "#b476cd",
    "技能2": "#da635d",
    "技能2+": "#da635d",
    "额外技能": "#c18469",
    "额外技能+": "#c18469",
    "SP连结爆发": Color.gold.value,
    "SP技能1": "#b476cd",
    "SP技能1+": "#b476cd",
    "SP技能2": "#da635d",
    "SP技能2+": "#da635d",
    "SP技能3": "#c18469",
}


async def draw_single_skill(
    skill_data: SkillData,
    action_data: List[SkillActionData],
    skill_type: str,
    level: int = 0,
    atk: int = 0,
):
    desc = get_action_description(action_data, skill_data, level, atk)
    process_action_data(desc)

    tags = {action.tag for action in desc[::-1] if action.tag}
    introduce = split_text(skill_data.description, 25)
    skill_text_max = 25
    height = (
        105
        + 20 * len(introduce)
        + 5  # 加点空隙
        + 25
        * sum(len(split_text(action.action_desc, skill_text_max)) for action in desc)
        + 10 * len(desc)
        - 10
    )

    base = Image.new("RGBA", (WIDTH, height), "#fef8f8")
    draw = ImageDraw.Draw(base)

    text_font_path = (
        FilePath.font_ms_bold.value
        if is_text_chinese(skill_data.description)
        else FilePath.font_jp.value
    )
    height = 10
    skill_name_font = ImageFont.truetype(text_font_path, 25)
    font_cn = ImageFont.truetype(FilePath.font_ms_bold.value, 15)
    font = ImageFont.truetype(text_font_path, 15)
    base.paste(
        Image.open(await get_skill_icon(skill_data.icon_type))
        .convert("RGBA")
        .resize((50, 50)),
        (MARGIN, height),
    )
    draw.text(
        (MARGIN + 60, height - 2),
        skill_data.name or skill_type,
        skill_type_color.get(skill_type, "#000000"),
        skill_name_font,
    )

    skill_info = skill_type
    if skill_data.skill_cast_time:
        skill_info += f"   准备时间: {skill_data.skill_cast_time}s"
    if level:
        skill_info += f"   技能等级: {level}"
    draw.text(
        (MARGIN + 60, height + 30),
        skill_info,
        "#000000",
        font_cn,
    )

    height += 55

    temp_width = 0
    for tag in tags:
        draw_text_with_base(
            draw,
            tag,
            MARGIN + temp_width,
            height,
            font_cn,
            "#ffffff",
            "#a5366f",
            margin=10,
        )
        x, _ = get_text_size(tag, font_cn)
        temp_width += x + 15
    height += 25
    draw.multiline_text(
        (MARGIN, height),
        "\n".join(introduce),
        "#000000",
        font,
    )
    height += 20 * len(introduce) + 10
    for action in desc:
        action_desc = split_text(action.action_desc, skill_text_max)
        # 绘制背景矩形（高度根据行数动态计算）
        draw.rounded_rectangle(
            (MARGIN, height, WIDTH - MARGIN, height + 25 * len(action_desc)),
            radius=10,
            fill="#f2dfe2",
        )

        # 用栈处理嵌套，默认状态颜色为黑色
        tag_stack = [("root", "#000000")]
        for text in action_desc:
            parts = []  # 存储 (文本段, 对应颜色) 的列表
            buffer = ""  # 缓冲普通文本
            # 定义开始/结束标记对及对应颜色

            for char in text:
                if char in TAG_PAIRS:  # 遇到左开标记
                    # 先将当前缓冲区内容 flush，按当前栈顶颜色输出
                    if buffer:
                        parts.append((buffer, tag_stack[-1][1]))
                        buffer = ""
                    # 将左开字符也加入输出，并使用对应颜色
                    parts.append((char, TAG_COLORS[char]))
                    # 入栈该标记以及新的颜色，后续文本使用新颜色
                    tag_stack.append((char, TAG_COLORS[char]))

                elif char in TAG_PAIRS.values():  # 遇到闭合标记
                    if len(tag_stack) > 1 and TAG_PAIRS.get(tag_stack[-1][0]) == char:
                        if buffer:
                            parts.append((buffer, tag_stack[-1][1]))
                            buffer = ""
                        # 输出闭合标记字符，并用当前颜色
                        parts.append((char, tag_stack[-1][1]))
                        # 弹出栈顶，恢复上一级颜色
                        tag_stack.pop()
                    else:
                        # 如果不匹配，则当作普通字符处理
                        buffer += char
                else:
                    buffer += char  # 普通字符加入缓冲区

            # 如果还有残留文本，追加到 parts
            if buffer:
                parts.append((buffer, tag_stack[-1][1]))

            # 根据 parts 逐段绘制文本，使用对应颜色，逐段更新 x 方向偏移量
            x_offset = MARGIN + 5
            for segment, color in parts:
                draw.text((x_offset, height), segment, color, font_cn)
                x_offset += draw.textlength(segment, font=font_cn)

            height += 25  # 每行更新高度
        height += 10  # 每个 action 间的间隔

    return base


async def draw_all_skill(
    skill_dict: Dict[str, List[int]],
    skill_type_dict: Dict[int, str],
    skill_data_dict: Dict[int, SkillData],
    action_dict: Dict[int, List[SkillActionData]],
    level_dict: Dict[int, int] = None,
    atk: int = 0,
):
    font = ImageFont.truetype(FilePath.font_ms_bold.value, 25)
    title1 = Image.new("RGBA", (WIDTH, 50), "#fef8f8")
    draw = ImageDraw.Draw(title1)
    draw.text(
        (WIDTH // 2 - MARGIN * 2, 10),
        "技能信息",
        "#a5366f",
        font,
    )
    imgs = [title1]
    for skill in skill_dict["normal"]:
        imgs.append(
            await draw_single_skill(
                skill_data_dict[skill],
                action_dict[skill],
                skill_type_dict[skill],
                level_dict.get(skill, 0) if level_dict else 0,
                atk,
            )
        )
    if skill_dict["sp"]:
        title2 = Image.new("RGBA", (WIDTH, 50), "#fef8f8")
        draw = ImageDraw.Draw(title2)
        draw.text(
            (WIDTH // 2 - MARGIN * 2, 10),
            "SP技能信息",
            "#a5366f",
            font,
        )
        imgs.append(title2)
        for skill in skill_dict["sp"]:
            imgs.append(
                await draw_single_skill(
                    skill_data_dict[skill],
                    action_dict[skill],
                    skill_type_dict[skill],
                )
            )
    return merge_pic(imgs)
