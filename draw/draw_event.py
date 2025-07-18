import datetime
from typing import Dict
from .util import draw_text_with_base
from ..download import get_enemy_icon, get_teaser_icon
from ..util import (
    convert2charid,
    is_text_chinese,
    parse_datetime,
    split_list,
    split_text,
    pcr_limit_type_dict,
)
from ..base import Color, FilePath
from PIL import Image, ImageDraw, ImageFont
from ..model import (
    BirthdayData,
    CalendarEvent,
    CampaignFreegachaData,
    ClanBattleData,
    EventData,
    GachaHistoryData,
    UnitInfo,
)
from hoshino.modules.priconne import chara

MARGIN = 30
WIDTH = 400
ALARM_CLOCK_ICON = (
    Image.open(FilePath.icon.value / "alarm_clock.png").convert("RGBA").resize((35, 35))
)
HOURGLASS_ICON = (
    Image.open(FilePath.icon.value / "hourglass.png").convert("RGBA").resize((25, 25))
)


def make_rounded_icon(icon: Image.Image, radius: int) -> Image.Image:
    """
    将图像处理为圆角。

    :param icon: 原始图像 (PIL.Image)
    :param radius: 圆角半径
    :return: 圆角处理后的图像
    """
    # 创建一个与图像大小相同的透明蒙版
    mask = Image.new("L", icon.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, icon.size[0], icon.size[1]), radius=radius, fill=255)

    # 将蒙版应用到图像上
    rounded_icon = Image.new("RGBA", icon.size, (0, 0, 0, 0))
    rounded_icon.paste(icon, (0, 0), mask)
    return rounded_icon


def draw_event_banner(
    draw: ImageDraw.ImageDraw,
    base: Image.Image,
    type_: str = "",
    type_color: str = "#ffffff",
    start_time: str = "",
    end_time: str = "",
) -> Image.Image:
    """
    在活动图像上绘制活动类型和时间。

    :param base: 原始图像 (PIL.Image)
    :param type_: 活动类型
    :param time: 活动时间
    :param is_in_progress: 是否正在进行中
    :return: 绘制后的图像
    """
    font_cn = ImageFont.truetype(FilePath.font_ms_bold.value, 15)
    width = MARGIN

    if type_:
        draw_text_with_base(
            draw,
            type_,
            MARGIN,
            5,
            font_cn,
            "#ffffff",
            type_color,
            margin=10,
        )
        width += int(font_cn.getlength(type_)) + 15

    if start_time:
        start = parse_datetime(start_time, fix_jp_time=False)
        time = start.strftime("%Y/%m/%d")
        draw_text_with_base(
            draw,
            time,
            width,
            5,
            font_cn,
            "#ffffff",
            Color.red.value,
            margin=10,
        )
        width += int(font_cn.getlength(time)) + 15

    if end_time:
        now = datetime.datetime.now()
        end = parse_datetime(end_time, fix_jp_time=False)
        total_days = (end - start).days + 1

        if now < start:
            left_time = start - now  # 距离开始时间
            color = Color.purple.value
            icon = HOURGLASS_ICON
            padding = 5
        elif now < end:
            left_time = end - datetime.datetime.now()  # 距离结束时间
            color = Color.red.value
            icon = ALARM_CLOCK_ICON
            padding = 0

        draw_text_with_base(
            draw,
            f"{total_days}天",
            width,
            5,
            font_cn,
            "#ffffff",
            color,
            margin=10,
        )
        width += int(font_cn.getlength(f"{total_days}天")) + 10

        base.paste(
            icon,
            (width + padding, padding),
            icon,
        )
        width += icon.size[0] - 5 + padding * 2

        time = f"{left_time.days}天"
        if left_time.seconds // 3600:
            time += f"{left_time.seconds // 3600}时"
        if left_time.seconds // 60 % 60:
            time += f"{left_time.seconds // 60 % 60}分"
        draw.text(
            (width, 7),
            time,
            color,
            font=font_cn,
        )
    return base


async def draw_story_event(event: EventData, type_: str) -> Image.Image:
    title = event.title.replace(" ", "").replace("\\n", "")
    title_list = split_text(title, 10)
    icon_height = int((WIDTH - 2 * MARGIN) * 0.42)
    height = icon_height + 100 + len(title_list) * 35
    icon = (
        Image.open(await get_teaser_icon(event.original_event_id, type_))
        .convert("RGBA")
        .resize((WIDTH - 2 * MARGIN, icon_height))
    )
    base = Image.new("RGBA", (WIDTH, height), "#fef8f8")
    draw = ImageDraw.Draw(base)

    font_path = (
        FilePath.font_ms_bold.value
        if is_text_chinese(event.title)
        else FilePath.font_jp.value
    )
    font = ImageFont.truetype(font_path, 20)
    font_cn = ImageFont.truetype(FilePath.font_ms_bold.value, 15)
    is_event_repeat = event.original_event_id == event.event_id
    base = draw_event_banner(
        draw,
        base,
        "活动" if is_event_repeat else "复刻",
        Color.orange.value if is_event_repeat else Color.gold.value,
        event.start_time,
        event.end_time,
    )
    draw.rounded_rectangle(
        (MARGIN, 35, WIDTH - MARGIN, height - 5),
        fill="#f2dee0",
        radius=10,
    )
    icon = make_rounded_icon(icon, radius=10)
    base.paste(
        icon,
        (MARGIN, 35),
        icon,
    )
    for i, text in enumerate(title_list):
        draw.text(
            (MARGIN + 10, icon_height + 35 + i * 35),
            text,
            "#000000",
            font=font,
        )

    icons = [
        (await chara.fromid(int(unit_id[1:])).get_icon())
        .open()
        .convert("RGBA")
        .resize((50, 50))
        for unit_id in set(event.unit_ids.split("-"))
        if unit_id[1:]
    ]
    for i, icon in enumerate(icons):
        base.paste(
            icon, (MARGIN + i * 65 + 15, icon_height + 35 + len(title_list) * 35)
        )
    draw.text(
        (WIDTH - MARGIN - 10, icon_height + 65 + len(title_list) * 35),
        event.end_time,
        "#000000",
        font=font_cn,
        anchor="ra",
    )

    return base


async def drwa_calendar_event(event: CalendarEvent):
    event_list = event.get_event_list()
    height = len(event_list) * 30 + 60
    base = Image.new("RGBA", (WIDTH, height), "#fef8f8")
    draw = ImageDraw.Draw(base)

    font_cn = ImageFont.truetype(FilePath.font_ms_bold.value, 15)

    draw_event_banner(
        draw,
        base,
        "",
        "",
        event.start_time,
        event.end_time,
    )

    draw.rounded_rectangle(
        (MARGIN, 35, WIDTH - MARGIN, height - 5),
        fill="#f2dee0",
        radius=10,
    )
    for i, event_data in enumerate(event_list):
        draw.text(
            (MARGIN + 10, 40 + i * 30),
            f"{event_data.title}{event_data.info}",
            "#000000",
            font=font_cn,
        )
        if event_data.multiple:
            text_length = int(
                draw.textlength(f"{event_data.title}{event_data.info}", font=font_cn)
            )
            draw.text(
                (MARGIN + text_length + 15, 40 + i * 30),
                event_data.multiple,
                event_data.color,
                font=font_cn,
            )
    draw.text(
        (WIDTH - MARGIN - 10, height - 30),
        event.end_time,
        "#000000",
        font=font_cn,
        anchor="ra",
    )
    return base


async def draw_free_gacha_event(event: CampaignFreegachaData):
    height = 85
    base = Image.new("RGBA", (WIDTH, height), "#fef8f8")
    draw = ImageDraw.Draw(base)
    font_cn = ImageFont.truetype(FilePath.font_ms_bold.value, 15)
    start_time = parse_datetime(event.start_time, fix_jp_time=False)
    end_time = parse_datetime(event.end_time, fix_jp_time=False)
    total_day = (end_time - start_time).days + 1
    draw_event_banner(
        draw,
        base,
        "",
        "",
        event.start_time,
        event.end_time,
    )
    draw.rounded_rectangle(
        (MARGIN, 35, WIDTH - MARGIN, height - 5),
        fill="#f2dee0",
        radius=10,
    )
    draw.text(
        (MARGIN + 10, 40),
        f"【免费十连】 {event.max_count or total_day} 次",
        "#000000",
        font=font_cn,
    )
    draw.text(
        (WIDTH - MARGIN - 10, height - 30),
        event.end_time,
        "#000000",
        font=font_cn,
        anchor="ra",
    )
    return base


async def draw_clan_battle_event(event: ClanBattleData):
    height = 125
    base = Image.new("RGBA", (WIDTH, height), "#fef8f8")
    draw = ImageDraw.Draw(base)
    font_cn = ImageFont.truetype(FilePath.font_ms_bold.value, 15)
    draw_event_banner(
        draw,
        base,
        "公会战",
        Color.orange.value,
        event.start_time,
        event.end_time,
    )

    draw.rounded_rectangle(
        (MARGIN, 35, WIDTH - MARGIN, height - 5),
        fill="#f2dee0",
        radius=10,
    )
    unit_ids = event.unit_ids.split("-")[:5]
    for i, unit_id in enumerate(unit_ids):
        icon = (
            Image.open(await get_enemy_icon(unit_id)).convert("RGBA").resize((50, 50))
        )
        base.paste(icon, (45 + i * 65, 45))

    draw.text(
        (WIDTH - MARGIN - 10, height - 30),
        event.end_time,
        "#000000",
        font=font_cn,
        anchor="ra",
    )

    return base


async def draw_birthday(event: BirthdayData):
    unit_ids = event.unit_ids.split("-")
    unit_ids_list = split_list(unit_ids, 5)
    height = len(unit_ids_list) * 60 + 50
    base = Image.new("RGBA", (WIDTH, height), "#fef8f8")
    draw = ImageDraw.Draw(base)
    font_cn = ImageFont.truetype(FilePath.font_ms_bold.value, 15)
    end_time = datetime.datetime.now().replace(
        month=event.month, day=event.day, hour=23, minute=59, second=59, microsecond=0
    )
    left_time = end_time - datetime.datetime.now()
    draw_text_with_base(
        draw,
        "生日",
        MARGIN,
        5,
        font_cn,
        Color.white.value,
        Color.orange.value,
        margin=10,
    )

    draw_text_with_base(
        draw,
        f"{event.month}月{event.day}日",
        MARGIN + 45,
        5,
        font_cn,
        "#ffffff",
        Color.purple.value if left_time.days else Color.red.value,
        margin=10,
    )

    if left_time.days:
        birthday_length = int(font_cn.getlength(f"{event.month}月{event.day}日"))
        base.paste(
            HOURGLASS_ICON,
            (MARGIN + birthday_length + 60, 5),
            HOURGLASS_ICON,
        )
        left_text = f"{left_time.days}天"
        if left_time.seconds // 3600:
            left_text += f"{left_time.seconds // 3600}时"
        if left_time.seconds // 60 % 60:
            left_text += f"{left_time.seconds // 60 % 60}分"
        draw.text(
            (MARGIN + birthday_length + 85, 7),
            left_text,
            Color.purple.value,
            font=font_cn,
        )

    draw.rounded_rectangle(
        (MARGIN, 35, WIDTH - MARGIN, height - 5),
        fill="#f2dee0",
        radius=10,
    )

    for i, unit_ids in enumerate(unit_ids_list):
        for j, unit_id in enumerate(unit_ids):

            icon = (
                (await chara.fromid(convert2charid(int(unit_id))).get_icon())
                .open()
                .convert("RGBA")
                .resize((50, 50))
            )
            base.paste(icon, (45 + j * 65, 45 + i * 60))

    return base


def get_gacha_event_type(
    gacha_name: str, description: str, limit_dict: Dict[int, UnitInfo]
) -> str:
    if gacha_name in {"プリンセスフェス", "公主祭典", "公主庆典"}:
        return "公主庆典", Color.green.value
    if "Anniversary" in gacha_name or "周年" in gacha_name:
        return "周年", Color.pink.value

    type_list = {
        pcr_limit_type_dict.get(unit_info.limit_type, "")
        for unit_info in limit_dict.values()
    }
    type_list = sorted(type_list)
    if any(keyword in description for keyword in ["復刻", "复刻", "自選"]):
        return "复刻" + "/".join(type_list), Color.gold.value

    return "/".join(type_list), Color.orange.value


async def draw_gacha_event(event: GachaHistoryData, limit_dict: Dict[int, UnitInfo]):
    unit_ids = event.unit_ids.split("-")
    unit_ids_list = split_list(unit_ids, 5)
    height = len(unit_ids_list) * 60 + 65
    base = Image.new("RGBA", (WIDTH, height), "#fef8f8")
    draw = ImageDraw.Draw(base)
    font_cn = ImageFont.truetype(FilePath.font_ms_bold.value, 15)
    type_, color = get_gacha_event_type(event.gacha_name, event.description, limit_dict)
    draw_event_banner(
        draw,
        base,
        type_,
        color,
        event.start_time,
        event.end_time,
    )

    draw.rounded_rectangle(
        (MARGIN, 35, WIDTH - MARGIN, height - 5),
        fill="#f2dee0",
        radius=10,
    )
    font_cn_small = ImageFont.truetype(FilePath.font_ms_bold.value, 12)
    for i, unit_ids in enumerate(unit_ids_list):
        for j, unit_id in enumerate(unit_ids):
            icon = (
                (await chara.fromid(convert2charid(int(unit_id))).get_icon())
                .open()
                .convert("RGBA")
                .resize((50, 50))
            )
            base.paste(icon, (45 + j * 65, 45 + i * 60))
            draw_text_with_base(
                draw,
                pcr_limit_type_dict.get(limit_dict[unit_id].limit_type, ""),
                45 + j * 65,
                77 + i * 60,
                font_cn_small,
                Color.white.value,
                color,
                margin=5,
            )

    draw.text(
        (WIDTH - MARGIN - 10, height - 30),
        event.end_time,
        "#000000",
        font=font_cn,
        anchor="ra",
    )

    return base
