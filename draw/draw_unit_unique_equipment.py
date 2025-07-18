from typing import List

from ..download import get_equipment_icon
from ..util import is_text_chinese, split_text
from .util import draw_text_with_base, merge_pic
from ..model import UniqueEquipInfo
from ..base import FilePath
from PIL import Image, ImageDraw, ImageFont

WIDTH = 500
MARGIN = 30


def get_equipment_effect(info: UniqueEquipInfo):
    effect = []
    if info.hp:
        effect.append(("HP", round(info.hp)))
    if info.atk:
        effect.append(("物理攻击", round(info.atk)))
    if info.magic_str:
        effect.append(("魔法攻击", round(info.magic_str)))
    if info.def_:
        effect.append(("物理防御", round(info.def_)))
    if info.magic_def:
        effect.append(("魔法防御", round(info.magic_def)))
    if info.physical_critical:
        effect.append(("物理暴击", round(info.physical_critical)))
    if info.magic_critical:
        effect.append(("魔法暴击", round(info.magic_critical)))
    if info.wave_hp_recovery:
        effect.append(("HP回复", round(info.wave_hp_recovery)))
    if info.wave_energy_recovery:
        effect.append(("TP回复", round(info.wave_energy_recovery)))
    if info.dodge:
        effect.append(("闪避", round(info.dodge)))
    if info.physical_penetrate:
        effect.append(("物理穿透", round(info.physical_penetrate)))
    if info.magic_penetrate:
        effect.append(("魔法穿透", round(info.magic_penetrate)))
    if info.life_steal:
        effect.append(("生命偷取", round(info.life_steal)))
    if info.hp_recovery_rate:
        effect.append(("回复上升", round(info.hp_recovery_rate)))
    if info.energy_recovery_rate:
        effect.append(("TP上升", round(info.energy_recovery_rate)))
    if info.energy_reduce_rate:
        effect.append(("TP减轻", round(info.energy_reduce_rate)))
    if info.accuracy:
        effect.append(("命中", round(info.accuracy)))
    return effect


async def draw_single_unique_equipment(
    unique_info: UniqueEquipInfo, level: int
) -> Image.Image:
    equip_icon_path = await get_equipment_icon(unique_info.equipment_id)
    equip_icon = Image.open(equip_icon_path).convert("RGBA").resize((100, 100))
    effect_list = get_equipment_effect(unique_info)
    description = split_text(unique_info.description.replace("\\n", ""), 20)
    height = 130 + 30 * len(description) + 35 * len(effect_list) // 2
    base = Image.new("RGBA", (WIDTH, height), "#fef8f8")
    draw = ImageDraw.Draw(base)
    font_path = (
        FilePath.font_ms_bold.value
        if is_text_chinese(unique_info.description)
        else FilePath.font_jp.value
    )
    font_cn = ImageFont.truetype(FilePath.font_ms_bold.value, 20)
    font = ImageFont.truetype(font_path, 20)
    base.paste(equip_icon, (MARGIN, 0))
    height = 110
    draw.text(
        (MARGIN + 110, 15),
        f"{unique_info.equipment_name}",
        "#a5366f",
        ImageFont.truetype(font_path, 25),
    )
    draw.text(
        (MARGIN + 110, 55),
        f"等级：{level}",
        "#000000",
        ImageFont.truetype(FilePath.font_ms_bold.value, 25),
    )
    draw.multiline_text((MARGIN, height), "\n".join(description), "#000000", font)
    height += 25 * len(description) + 10
    height += 10
    for i, effect in enumerate(effect_list):
        if i % 2 == 0:
            draw_text_with_base(
                draw,
                effect[0],
                MARGIN,
                height,
                font_cn,
                "#ffffff",
                "#a5366f",
                margin=10,
            )
            draw.text(
                (WIDTH // 2 - MARGIN, height + 5),
                str(effect[1]),
                "#000000",
                font_cn,
                anchor="rt",
            )
        else:
            draw_text_with_base(
                draw,
                effect[0],
                WIDTH // 2,
                height,
                font_cn,
                "#ffffff",
                "#a5366f",
                margin=10,
            )
            draw.text(
                (WIDTH - MARGIN, height + 5),
                str(effect[1]),
                "#000000",
                font_cn,
                anchor="rt",
            )
            height += 35

    return base


async def draw_unique_equipment(
    unique_info: List[UniqueEquipInfo], level_list: List[int]
) -> Image.Image:

    img_list = [
        await draw_single_unique_equipment(info, level)
        for info, level in zip(unique_info, level_list)
    ]

    return merge_pic(img_list, "vertical")
