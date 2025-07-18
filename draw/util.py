from typing import List
from PIL import ImageFont, ImageDraw, Image


def get_text_size(text, font: ImageFont.ImageFont):
    bbox = font.getbbox(str(text))
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def adjust_color_brightness(rgb_color, factor):
    """
    调整颜色亮度：
    - factor = 0：原色
    - factor > 0：向白色靠近（变淡）
    - factor < 0：向黑色靠近（变深）
    """
    if factor >= 0:
        return tuple(int(c + (255 - c) * factor) for c in rgb_color)
    else:
        return tuple(int(c * (1 + factor)) for c in rgb_color)


def draw_text_shadow(
    draw: ImageDraw.ImageDraw,
    text,
    x,
    y,
    font: ImageFont,
    shadow_color=(105, 105, 105),
    font_color=(255, 255, 255),
    thick=2,
):
    draw.text((x - thick, y - thick), text, font=font, fill=shadow_color)
    draw.text((x + thick, y + thick), text, font=font, fill=shadow_color)
    draw.text((x + thick, y - 1), text, font=font, fill=shadow_color)
    draw.text((x - thick, y + thick), text, font=font, fill=shadow_color)
    draw.text((x, y), text, font_color, font)


def draw_text_with_base(
    draw: ImageDraw.ImageDraw,
    text: str,
    x,
    y,
    font: ImageFont.ImageFont,
    font_colour=(255, 255, 255),
    base_colour=(0, 0, 0),
    margin=20,
):
    x_, y_ = get_text_size(text, font)
    if text.isascii():
        _, y_ = get_text_size("环奈", font)  # 修正英文字符的高度

    draw.rounded_rectangle(
        (
            x,
            y,
            x + x_ + margin,
            y + y_ + margin,
        ),
        fill=base_colour,
        radius=5,
    )
    draw.text(
        (x + (x_ + margin) // 2, y + (y_ + margin) // 2),
        text,
        font_colour,
        font,
        anchor="mm",
    )


def merge_pic(pic_list: List[Image.Image], direction: str = "vertical"):
    """
    沿长度方向合并图片。
    :param pic_list: list，图片列表
    :param direction: str，合并方向，"horizontal" 或 "vertical"
    :return: Image.Image，合并后的图片
    """
    if not pic_list:
        return None

    if direction == "horizontal":
        height = max(pic.size[1] for pic in pic_list)
        width = sum(pic.size[0] for pic in pic_list)
    else:
        width = max(pic.size[0] for pic in pic_list)
        height = sum(pic.size[1] for pic in pic_list)

    base = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    temp = 0
    for pic in pic_list:
        if direction == "horizontal":
            base.paste(pic, (temp, 0))
            temp += pic.size[0]
        else:
            base.paste(pic, (0, temp))
            temp += pic.size[1]

    return base
