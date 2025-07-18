from typing import List
from ..table import EnemyParameter, UnitEnemyData
from ..util import is_text_chinese, split_text
from .util import draw_text_with_base
from ..base import FilePath, Color
from PIL import Image, ImageDraw, ImageFont

WIDTH = 500
MARGIN = 30


def draw_full_parameter_info(
    draw: ImageDraw.ImageDraw,
    parameter: EnemyParameter,
    height: int,
    font: ImageFont.FreeTypeFont,
):
    draw_text_with_base(
        draw, "HP", MARGIN, height, font, "#ffffff", Color.red.value, margin=10
    )
    draw.text(
        (WIDTH - MARGIN, height + 8), str(parameter.hp), "#000000", font, anchor="rt"
    )
    height += 30

    draw_text_with_base(
        draw, "命中", MARGIN, height, font, "#ffffff", Color.red.value, margin=10
    )
    draw.text(
        (WIDTH - MARGIN, height + 8),
        str(parameter.accuracy),
        "#000000",
        font,
        anchor="rt",
    )
    height += 30

    draw_text_with_base(
        draw, "物理攻击力", MARGIN, height, font, "#ffffff", Color.red.value, margin=10
    )
    draw.text(
        (WIDTH - MARGIN, height + 8), str(parameter.atk), "#000000", font, anchor="rt"
    )
    height += 30

    draw_text_with_base(
        draw, "魔法攻击力", MARGIN, height, font, "#ffffff", Color.red.value, margin=10
    )
    draw.text(
        (WIDTH - MARGIN, height + 8),
        str(parameter.magic_str),
        "#000000",
        font,
        anchor="rt",
    )
    height += 30

    draw_text_with_base(
        draw, "物理防御力", MARGIN, height, font, "#ffffff", Color.red.value, margin=10
    )
    draw.text(
        (WIDTH - MARGIN, height + 8), str(parameter.def_), "#000000", font, anchor="rt"
    )
    height += 30

    draw_text_with_base(
        draw, "魔法防御力", MARGIN, height, font, "#ffffff", Color.red.value, margin=10
    )
    draw.text(
        (WIDTH - MARGIN, height + 8),
        str(parameter.magic_def),
        "#000000",
        font,
        anchor="rt",
    )
    height += 30
    draw_text_with_base(
        draw, "TP上升", MARGIN, height, font, "#ffffff", Color.red.value, margin=10
    )
    draw.text(
        (WIDTH - MARGIN, height + 8),
        str(parameter.energy_recovery_rate),
        "#000000",
        font,
        anchor="rt",
    )
    height += 30 + 10  # 额外的间距
    return height


async def draw_enemy_introduce(
    main_parameter: EnemyParameter,
    sub_parameters: List[EnemyParameter],
):
    length = 10
    length += 90 + len(sub_parameters) * (30 * 7 + 55) if sub_parameters else 30 * 7
    base = Image.new("RGBA", (WIDTH, length), "#fef8f8")
    draw = ImageDraw.Draw(base)
    text_font_path = (
        FilePath.font_ms_bold.value
        if is_text_chinese(main_parameter.name)
        else FilePath.font_jp.value
    )

    font_cn = ImageFont.truetype(FilePath.font_ms_bold.value, 15)

    height = 0
    if sub_parameters:
        draw_text_with_base(
            draw, "HP", MARGIN, height, font_cn, "#ffffff", Color.red.value, margin=10
        )
        draw.text(
            (WIDTH - MARGIN, height + 10),
            str(main_parameter.hp),
            "#000000",
            font_cn,
            anchor="rt",
        )
        height += 30
        draw_text_with_base(
            draw, "命中", MARGIN, height, font_cn, "#ffffff", Color.red.value, margin=10
        )
        draw.text(
            (WIDTH - MARGIN, height + 10),
            str(main_parameter.accuracy),
            "#000000",
            font_cn,
            anchor="rt",
        )
        height += 30
        draw_text_with_base(
            draw,
            "TP上升",
            MARGIN,
            height,
            font_cn,
            "#ffffff",
            Color.red.value,
            margin=10,
        )
        draw.text(
            (WIDTH - MARGIN, height + 10),
            str(main_parameter.energy_recovery_rate),
            "#000000",
            font_cn,
            anchor="rt",
        )
        height += 30
        name_font = ImageFont.truetype(text_font_path, 25)
        for parameter in sub_parameters:
            draw.text(
                (WIDTH // 2, height),
                f"{parameter.name}",
                Color.red.value,
                name_font,
                anchor="mt",
            )
            height += 45
            height = draw_full_parameter_info(draw, parameter, height, font_cn)
    else:
        height = draw_full_parameter_info(draw, main_parameter, height, font_cn)

    draw = ImageDraw.Draw(base)
    return base
