from ..download import get_enemy_icon
from ..util import convert2charid
from ..base import FilePath
from PIL import Image, ImageDraw, ImageFont
from hoshino.modules.priconne import chara

MARGIN = 30


async def draw_char_icon(unit_id: int, width: int = 400) -> Image.Image:
    unit_id = convert2charid(unit_id)
    base = Image.new("RGBA", (width, 120), "#fef8f8")
    unit = chara.fromid(unit_id)
    name = unit.name
    font = ImageFont.truetype(FilePath.font_ms_bold.value, 35)
    icon = (await unit.get_icon()).open().convert("RGBA").resize((100, 100))
    base.paste(icon, (MARGIN, 10))
    draw = ImageDraw.Draw(base)
    draw.text((MARGIN + 110, 35), name, "#a5366f", font)
    return base


async def draw_enemy_icon(unit_id: int, name: str, width: int = 400) -> Image.Image:
    base = Image.new("RGBA", (width, 120), "#fef8f8")
    icon = Image.open(await get_enemy_icon(unit_id)).convert("RGBA").resize((100, 100))
    font = ImageFont.truetype(FilePath.font_ms_bold.value, 35)
    base.paste(icon, (MARGIN, 10))
    draw = ImageDraw.Draw(base)
    draw.text((MARGIN + 110, 35), name, "#a5366f", font)
    return base
