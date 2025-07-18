from ..util import convert2charid, is_text_chinese, split_text
from .util import get_text_size, draw_text_with_base
from ..model import UnitInfo
from ..base import FilePath, Color
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1408
MARGIN = 30


async def draw_introduce(info: UnitInfo):
    id_ = convert2charid(info.unit_id)

    # 获得文案
    catch_copy_list = split_text(info.catch_copy, 20)
    introduce = split_text(info.intro.replace("\\n", ""), 35)
    self_text = (
        split_text(info.self_text.replace("\\n", ""), 35)
        if (
            info.self_text
            and "test" not in info.self_text
            and "？" not in info.self_text
        )
        else []
    )
    length = len(catch_copy_list) * 75 + len(introduce) * 45 + len(self_text) * 45 + 360
    if self_text:
        length += 60  # 介绍标题

    base = Image.new("RGBA", (WIDTH, length), "#fef8f8")
    draw = ImageDraw.Draw(base)
    text_font_path = (
        FilePath.font_ms_bold.value
        if is_text_chinese(info.unit_name)
        else FilePath.font_jp.value
    )
    font_cn = ImageFont.truetype(FilePath.font_ms_bold.value, 55)
    font = ImageFont.truetype(text_font_path, 55)

    height = 25

    for catch_copy in catch_copy_list:
        x, y = get_text_size(catch_copy, font)
        draw.text(((WIDTH - x) // 2, height), catch_copy, Color.red.value, font)
        height += y + 20
    height += 10

    font_cn = ImageFont.truetype(FilePath.font_ms_bold.value, 35)
    font = ImageFont.truetype(text_font_path, 35)
    draw.multiline_text(
        (MARGIN, height),
        "\n".join(introduce),
        "#000000",
        font,
        spacing=15,
        align="left",
    )
    height += 20 + len(introduce) * 45

    draw_text_with_base(
        draw, "编号", MARGIN, height, font_cn, "#ffffff", Color.red.value
    )
    draw.text((WIDTH - MARGIN, height + 10), str(id_), "#000000", font, anchor="rt")
    height += 60

    draw_text_with_base(
        draw, "现实名字", MARGIN, height, font_cn, "#ffffff", Color.red.value
    )
    draw.text(
        (WIDTH - MARGIN, height + 10), info.actual_name, "#000000", font, anchor="rt"
    )
    height += 60

    draw_text_with_base(
        draw, "公会", MARGIN, height, font_cn, "#ffffff", Color.red.value
    )
    draw.text((WIDTH - MARGIN, height + 10), info.guild, "#000000", font, anchor="rt")
    height += 60

    draw_text_with_base(
        draw, "兴趣", MARGIN, height, font_cn, "#ffffff", Color.red.value
    )
    draw.text(
        (WIDTH - MARGIN, height + 10), info.favorite, "#000000", font, anchor="rt"
    )
    height += 60

    draw_text_with_base(
        draw, "血型", MARGIN, height, font_cn, "#ffffff", Color.red.value
    )
    draw.text(
        (WIDTH // 2 - MARGIN, height + 10),
        f"{info.blood_type}型",
        "#000000",
        font_cn,
        anchor="rt",
    )

    draw_text_with_base(
        draw, "种族", WIDTH // 2, height, font_cn, "#ffffff", Color.red.value
    )
    draw.text((WIDTH - MARGIN, height + 10), info.race, "#000000", font, anchor="rt")
    height += 60

    if self_text:
        draw_text_with_base(
            draw, "介绍", MARGIN, height, font_cn, "#ffffff", Color.red.value
        )
        height += 60
        draw.multiline_text(
            (MARGIN, height),
            "\n".join(self_text),
            "#000000",
            font,
            spacing=15,
            align="left",
        )

    return base
