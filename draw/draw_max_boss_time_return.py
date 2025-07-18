from typing import Dict, List, Tuple

from .util import draw_text_with_base, adjust_color_brightness, merge_pic

from ..base import FilePath
from ..util import phase_dict_reverse
from PIL import Image, ImageDraw, ImageFont
from ..base import Color

WIDTH = 3200

color_list = [Color.green.value, Color.gold.value, Color.purple.value, Color.red.value]


def draw_title(time: str, clan_battle_id: int) -> str:
    """
    绘制标题
    :param time: 时间字符串
    :return: 标题字符串
    """
    title = f"{clan_battle_id}期满补线计算（{time}）"
    height = 200
    base = Image.new("RGBA", (WIDTH, height), "#fef8f8")
    draw = ImageDraw.Draw(base)
    font_cn = ImageFont.truetype(FilePath.font_ms_bold.value, 55)
    draw.text(
        (WIDTH // 2, 25),
        title,
        "#000000",
        font_cn,
        anchor="mt",
    )
    pad = "\t" * 8
    draw_text_with_base(
        draw, f"{pad}周目{pad}", 30, 100, font_cn, base_colour=Color.red.value
    )
    draw_text_with_base(
        draw, "血量(万)", 420, 100, font_cn, base_colour=Color.red.value
    )
    pad = "\t" * 3
    for i in range(1, 9):
        draw_text_with_base(
            draw,
            f"{pad}{i}+满补{pad}",
            350 + i * 315,
            100,
            font_cn,
            base_colour=Color.red.value,
        )
    return base


def draw_single_boss_max_time_return(
    phase: int,
    damage_data: List[List[int]],
    hp_data: List[int],
    phase_lap_from_to: Tuple[int, int],
    color: str = "#000000",
) -> str:
    """
    根据时间和BOSS血量计算伤害
    :param boss_hp: BOSS血量
    :param n: 满补线数量
    :return: 计算出的伤害值
    """
    height = 350
    color = color.lstrip("#")
    rgb_color = [int(color[i : i + 2], 16) for i in (0, 2, 4)]

    color_base = adjust_color_brightness(rgb_color, 0.6)  # 原 alpha 100 对应 ≈ 淡化 60%
    color_title1 = adjust_color_brightness(rgb_color, 0.3)  # 原 alpha 200 ≈ 变淡 30%
    color_title2 = adjust_color_brightness(rgb_color, 0.4)  # 原 alpha 150 ≈ 变淡 40%

    base = Image.new(
        "RGBA",
        (WIDTH, height),
        color_base,  # 半透明背景
    )
    draw = ImageDraw.Draw(base)
    draw.rectangle((0, 0, 300, height), fill=color_title1)
    draw.rectangle((300, 0, WIDTH, height // 5), fill=color_title2)
    draw.rectangle((300, height // 5 * 4, WIDTH, height), fill=color_title2)
    draw.rectangle((300, height // 5 * 2, WIDTH, height // 5 * 3), fill=color_title2)

    font_cn = ImageFont.truetype(FilePath.font_ms_bold.value, 55)
    phase = phase_dict_reverse[phase]
    draw.text(
        (80, height // 2),
        (
            f"{phase} {phase_lap_from_to[0]}~{phase_lap_from_to[1]}"
            if phase_lap_from_to[1] != -1
            else f"{phase} {phase_lap_from_to[0]}+"
        ),
        "#000000",
        font_cn,
        anchor="lm",
    )
    text_color: str = "#000000"
    draw.multiline_text(
        (310, height // 2),
        "\n".join([f"{phase}{i}" for i in range(1, 5 + 1)]),
        fill=text_color,
        font=font_cn,
        anchor="lm",
        align="center",
        spacing=10,
    )
    draw.multiline_text(
        (600, height // 2),
        "\n".join([f"{hp // 10000}" for hp in hp_data]),
        fill=text_color,
        font=font_cn,
        anchor="rm",
        align="right",
        spacing=10,
    )
    for i, line in enumerate(damage_data):
        for j, damage in enumerate(line):
            x = 920 + j * 315
            y = i * 70 + 20
            draw.text(
                (x, y),
                f"{damage/10000:.2f}",
                fill=text_color,
                font=font_cn,
                anchor="rt",
            )
    return base


def draw_max_boss_time_return(
    damage_dict: Dict[int, List[List[int]]],
    boss_hp_dict: Dict[int, List[int]],
    phase_lap_dict: Dict[int, Tuple[int, int]],
    clan_battle_id: int,
    time: str,
) -> Image.Image:
    """
    绘制满补线计算结果
    :param data: 包含所有阶段数据的字典
    :param time: 会战时间字符串
    :return: 绘制好的图片
    """
    imgs = [draw_title(time, clan_battle_id)]
    color_num = len(color_list)
    imgs += [
        draw_single_boss_max_time_return(
            phase,
            damage_dict[phase],
            boss_hp_dict[phase],
            phase_lap_dict[phase],
            color_list[i % color_num],
        )
        for i, phase in enumerate(damage_dict)
    ]
    img = merge_pic(imgs)
    kanna_log = (
        Image.open(FilePath.icon.value / "kailu.png").convert("RGBA").resize((600, 750))
    )
    img.paste(kanna_log, (2600, 175), mask=kanna_log)
    return img
