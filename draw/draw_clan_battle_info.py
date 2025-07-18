import datetime
from typing import Dict, List

from ..download import get_enemy_icon
from .util import draw_text_with_base, merge_pic
from ..model import ClanBattleData
from ..base import FilePath, Color
from PIL import Image, ImageDraw, ImageFont

WIDTH = 400
MARGIN = 30


async def draw_clan_info(
    clan_info: List[ClanBattleData], count_dict: Dict[int, Dict[int, List[str]]]
):
    return merge_pic(
        [
            await draw_single_clan_info(clan, count_dict[clan.clan_battle_id])
            for clan in clan_info
        ]
    )


async def draw_single_clan_info(
    clan_info: ClanBattleData, count_dict: Dict[int, List[str]]
):
    height = 110
    base = Image.new("RGBA", (WIDTH, height), "#fef8f8")
    draw = ImageDraw.Draw(base)
    font_cn = ImageFont.truetype(FilePath.font_ms_bold.value, 15)
    font_big = ImageFont.truetype(FilePath.font_ms_bold.value, 35)
    draw_text_with_base(
        draw,
        datetime.datetime.strptime(clan_info.start_time, "%Y/%m/%d %H:%M:%S").strftime(
            "%Y年%m月"
        ),
        MARGIN,
        5,
        font_cn,
        "#ffffff",
        Color.red.value,
        margin=10,
    )
    draw_text_with_base(
        draw,
        f"{clan_info.min_phase}-{clan_info.max_phase}阶段",
        MARGIN + 100,
        5,
        font_cn,
        "#ffffff",
        "#ed6c51",
        margin=10,
    )
    draw.text(
        (MARGIN + 170, 7),
        f"会战ID: {clan_info.clan_battle_id}",
        "#000000",
        font=font_cn,
    )
    draw.rounded_rectangle(
        (MARGIN, 35, WIDTH - 2 * MARGIN, 105),
        fill="#f2dee0",
        radius=10,
    )
    unit_ids = clan_info.unit_ids.split("-")[:5]
    enemy_ids = clan_info.enemy_ids.split("-")[-5:]
    for i, unit_id in enumerate(unit_ids):
        icon = (
            Image.open(await get_enemy_icon(unit_id)).convert("RGBA").resize((50, 50))
        )
        base.paste(icon, (40 + i * 60, 45))
        if num := len([_ for _ in count_dict[int(enemy_ids[i])] if _ and int(_)]):
            draw.text(
                (55 + i * 60, 45),
                str(num),
                "#ffffff",
                font=font_big,
            )

    return base
