from PIL import Image, ImageFont, ImageDraw
import colorsys

from ..base import FilePath
from ..model import UnitInfo
from ..util import (
    convert2charid,
    is_text_chinese,
    limit_type_int2str,
    search_type_distance2str,
)
from ..download import get_pcr_fullcard
from .util import get_text_size, draw_text_shadow

base_dict = {
    "常驻": (136, 136, 136),
    "限定": (239, 95, 168),
    "兑换": (66, 170, 240),
    "活动": (250, 90, 90),
    "魔法": (148, 90, 254),
    "物理": (255, 188, 51),
    "前卫": (250, 90, 90),
    "中卫": (255, 188, 51),
    "后卫": (66, 170, 240),
}

font_colour = (255, 255, 255)


def get_dominant_color(image: Image.Image):
    image = image.copy()
    image.thumbnail((200, 200))  # 生成缩略图，减少计算量，减小cpu压力
    max_score = 0
    dominant_color = None
    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        # 跳过纯黑色
        if a == 0:
            continue
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
        y = (y - 16.0) / (235 - 16)
        # 忽略高亮色
        if y > 0.9:
            continue
        score = (saturation + 0.1) * count
        if score > max_score:
            max_score = score
            dominant_color = (r, g, b, 123)
    return dominant_color


def get_base_img(save_path):
    img = (
        Image.open(save_path).convert("RGBA").copy().resize((1408, 792), Image.LANCZOS)
    )
    base = Image.open(FilePath.icon.value / "base.png").convert("RGBA")
    mask = Image.open(FilePath.icon.value / "mask.png").convert("RGBA")
    mask_colour = Image.new("RGBA", mask.size, get_dominant_color(img))
    mask.paste(mask_colour, mask=mask)  # 生成遮罩
    base.paste(img, mask=base)  # 生成底图
    width, height = img.size
    base.paste(mask_colour, (width - 566, 0), mask=mask)
    return base, width, height


def text_base(img, width, height, base, target_width=141):

    temple = Image.open(FilePath.icon.value / "temple.png")
    if target_width > 141:
        orig_width, orig_height = temple.size
        left = orig_width // 3
        right = orig_width - left

        # 切出三块
        A = temple.crop((0, 0, left, orig_height))
        B = temple.crop((left, 0, right, orig_height))
        C = temple.crop((right, 0, orig_width, orig_height))

        # 计算中间B的新宽度
        new_B_width = target_width - A.width - C.width
        B = B.resize((new_B_width, orig_height))

        # 拼接
        temple = Image.new("RGBA", (target_width, orig_height))
        temple.paste(A, (0, 0))
        temple.paste(B, (A.width, 0))
        temple.paste(C, (A.width + B.width, 0))

    mask = Image.new("RGBA", temple.size, base)

    img.paste(mask, (int(width), int(height)), mask=temple)


async def draw_fullcard(info: UnitInfo, unique_num=0):
    id_ = convert2charid(info.unit_id)
    save_path = await get_pcr_fullcard(id_)
    base, width, height = get_base_img(save_path)

    # 文案处理
    font = ImageFont.truetype(FilePath.font_ms_bold.value, 48)

    draw = ImageDraw.Draw(base)

    draw.multiline_text(
        (width * 0.85, height / 15),
        f"{info.age_int if info.age_int != -1 else '?'}岁\n"
        f"{info.birth_month_int if info.birth_month_int != -1 else '?'}月{info.birth_day_int if info.birth_day_int != -1 else '?'}日\n"
        f"{info.weight_int if info.weight_int != -1 else '?'}KG\n"
        f"{info.height_int if info.height_int !=-1 else '?'}CM",
        font_colour,
        font,
        align="right",
    )

    font = ImageFont.truetype(FilePath.font_fz.value, 42)
    if unique_num:
        unique = (
            Image.open(FilePath.icon.value / f"ic_unique_equip{unique_num}.png")
            .copy()
            .resize((60, 60), Image.LANCZOS)
        )
        base.paste(
            unique,
            (int(width * 0.82), int(height * 0.76 - 53)),
            mask=unique,
        )
    is_limit = limit_type_int2str(info.limit_type)
    x, y = get_text_size(is_limit, font)
    text_base(
        base,
        width * 0.95 - x / 2 - 141 / 2,
        height * 0.75 - 47,
        base_dict[is_limit],
    )
    draw.text((width * 0.95 - x, height * 0.75 - y), is_limit, font_colour, font)

    atk_type = "物理" if info.atk_type == 1 else "魔法"
    x, y = get_text_size(atk_type, font)
    text_base(
        base,
        width * 0.95 - x / 2 - 119,
        height * 0.79,
        base_dict[atk_type],
        target_width=200,
    )
    draw.text((width * 0.89, height * 0.8), atk_type, font_colour, font, align="right")
    atk_type_sign = Image.open(FilePath.icon.value / f"{atk_type}.png").copy()
    base.paste(
        atk_type_sign,
        (int(width * 0.85), int(height * 0.8)),
        mask=atk_type_sign,
    )
    type_ = search_type_distance2str(info.search_area_width)
    search_area_width = f"{info.search_area_width}"
    bbox = font.getbbox(search_area_width)
    x, y = bbox[2] - bbox[0], bbox[3] - bbox[1]
    text_base(base, width * 0.7, height * 0.79, base_dict[type_], target_width=180)
    draw.text(
        (width * 0.76, height * 0.8),
        search_area_width,
        font_colour,
        font,
        align="right",
    )

    sign = (
        Image.open(FilePath.icon.value / f"{type_}.png")
        .copy()
        .resize((60, 60), Image.LANCZOS)
    )
    base.paste(
        sign,
        (int(width * 0.7) + 20, int(height * 0.77) + 20),
        mask=sign,
    )

    font = ImageFont.truetype(FilePath.font_ms_bold.value, 60)
    draw_text_shadow(
        draw,
        info.unit_name,
        width * 0.02,
        height * 0.85,
        (
            font
            if is_text_chinese(info.unit_name)
            else ImageFont.truetype(FilePath.font_jp.value, font.size)
        ),
    )

    font = ImageFont.truetype(FilePath.font_ms_regular.value, 30)
    draw.text(
        (width * 0.97, height / 10 * 9),
        info.unit_start_time.split()[0],
        font_colour,
        font,
        anchor="rt",
    )

    draw_text_shadow(
        draw,
        f"CV：{info.voice}",
        width * 0.02,
        height * 0.8,
        (
            font
            if is_text_chinese(info.unit_name)
            else ImageFont.truetype(FilePath.font_jp.value, font.size)
        ),
    )

    font = ImageFont.truetype(FilePath.font_ms_regular.value, 16)
    draw.text(
        (width * 0.97, height / 10 * 9 + 40),
        "设计参考来源于PCR TOOL",
        font_colour,
        font,
        anchor="rt",
    )

    return base
