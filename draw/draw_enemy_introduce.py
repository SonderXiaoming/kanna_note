from typing import List, Optional
from ..table import EnemyParameter, TalentWeakness
from .util import draw_text_with_base
from ..base import FilePath, Color, TalentType
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
        draw, "HP", MARGIN, height, font, "#ffffff", Color.primary.value, margin=10
    )
    draw.text(
        (WIDTH - MARGIN, height + 8), str(parameter.hp), "#000000", font, anchor="rt"
    )
    height += 30

    draw_text_with_base(
        draw, "命中", MARGIN, height, font, "#ffffff", Color.primary.value, margin=10
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
        draw, "物理攻击力", MARGIN, height, font, "#ffffff", Color.primary.value, margin=10
    )
    draw.text(
        (WIDTH - MARGIN, height + 8), str(parameter.atk), "#000000", font, anchor="rt"
    )
    height += 30

    draw_text_with_base(
        draw, "魔法攻击力", MARGIN, height, font, "#ffffff", Color.primary.value, margin=10
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
        draw, "物理防御力", MARGIN, height, font, "#ffffff", Color.primary.value, margin=10
    )
    draw.text(
        (WIDTH - MARGIN, height + 8), str(parameter.def_), "#000000", font, anchor="rt"
    )
    height += 30

    draw_text_with_base(
        draw, "魔法防御力", MARGIN, height, font, "#ffffff", Color.primary.value, margin=10
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
        draw, "TP上升", MARGIN, height, font, "#ffffff", Color.primary.value, margin=10
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
    talent_weakness: Optional[TalentWeakness] = None,
    text_font_path: str = FilePath.font_ms_bold.value,
):
    length = 10
    length += 90 + len(sub_parameters) * (30 * 7 + 55) if sub_parameters else 30 * 7
    length += 40 if talent_weakness else 0
    base = Image.new("RGBA", (WIDTH, length), "#fef8f8")
    draw = ImageDraw.Draw(base)

    font_cn = ImageFont.truetype(FilePath.font_ms_bold.value, 15)

    height = 0
    if talent_weakness:
        font_weakness = ImageFont.truetype(FilePath.font_ms_bold.value, 20)
        width = MARGIN
        for i, weakness_percent in enumerate([
            talent_weakness.talent_1,
            talent_weakness.talent_2,
            talent_weakness.talent_3,
            talent_weakness.talent_4,
            talent_weakness.talent_5,
        ], start=1):
            if weakness_percent == 100:
                continue
            weakness = TalentType.get(i)
            weakness_text = f"{weakness.name}+{weakness_percent}%"
            draw_text_with_base(
                draw,
                weakness_text,
                width,
                height,
                font_weakness,
                "#ffffff",
                weakness.color,
                margin=10,
            )
            width += 110
        height += 40
    if sub_parameters:
        draw_text_with_base(
            draw, "HP", MARGIN, height, font_cn, "#ffffff", Color.primary.value, margin=10
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
            draw, "命中", MARGIN, height, font_cn, "#ffffff", Color.primary.value, margin=10
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
            Color.primary.value,
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
                Color.primary.value,
                name_font,
                anchor="mt",
            )
            height += 45
            height = draw_full_parameter_info(draw, parameter, height, font_cn)
    else:
        height = draw_full_parameter_info(draw, main_parameter, height, font_cn)

    height += 20
    
    draw = ImageDraw.Draw(base)
    return base
