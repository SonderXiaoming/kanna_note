import math
from typing import Dict, List
from ..util import is_text_chinese
from .util import draw_text_with_base
from ..model import CharaStoryStatusData
from ..base import FilePath, STORY_STATE_DICT
from PIL import Image, ImageDraw, ImageFont
from hoshino.modules.priconne import chara

WIDTH = 400
MARGIN = 30


async def draw_story(story_dict: Dict[int, List[CharaStoryStatusData]]):
    show_story = []
    for stories in story_dict.values():
        for story in stories:
            if temp := len(
                {
                    t
                    for t in (
                        story.status_type_1,
                        story.status_type_2,
                        story.status_type_3,
                        story.status_type_4,
                        story.status_type_5,
                    )
                    if t
                }
            ):
                show_story.append(math.ceil(temp / 2))
    height = (
        len(story_dict.keys()) * 105 + 30 * len(show_story) + 25 * sum(show_story)
    ) + 20
    base = Image.new("RGBA", (WIDTH, height), "#fef8f8")
    draw = ImageDraw.Draw(base)
    text_font_path = (
        FilePath.font_ms_bold.value
        if is_text_chinese(next(iter(story_dict.values()))[0].title)
        else FilePath.font_jp.value
    )
    font_cn = ImageFont.truetype(FilePath.font_ms_bold.value, 15)
    font = ImageFont.truetype(text_font_path, 15)
    height = 20
    for unit_id, story_list in story_dict.items():
        name, num = story_list[0].title.split()
        icon = (
            (await chara.fromid(unit_id).get_icon())
            .open()
            .convert("RGBA")
            .resize((100, 100))
        )
        base.paste(icon, (MARGIN, height))
        draw.text((MARGIN + 110, height + 30), name, "#a5366f", font)
        height += 105
        for story in story_list:
            status_list = [
                (t, getattr(story, f"status_rate_{i}"))
                for i in range(1, 6)
                if (t := getattr(story, f"status_type_{i}"))
            ]
            if not status_list:
                continue
            draw.text(
                (MARGIN, height),
                f"{story.title.split()[-1]} {story.sub_title}",
                "#000000",
                font,
            )
            height += 25
            for i, (status, rate) in enumerate(status_list):
                if i % 2 == 0:
                    draw_text_with_base(
                        draw,
                        STORY_STATE_DICT[status],
                        MARGIN,
                        height,
                        font_cn,
                        "#ffffff",
                        "#a5366f",
                        margin=10,
                    )
                    draw.text(
                        (WIDTH // 2 - MARGIN, height + 8),
                        str(rate),
                        "#000000",
                        font_cn,
                        anchor="rt",
                    )
                else:
                    draw_text_with_base(
                        draw,
                        STORY_STATE_DICT[status],
                        WIDTH // 2,
                        height,
                        font_cn,
                        "#ffffff",
                        "#a5366f",
                        margin=10,
                    )
                    draw.text(
                        (WIDTH - MARGIN, height + 8),
                        str(rate),
                        "#000000",
                        font_cn,
                        anchor="rt",
                    )
                    height += 30
            height += 30 if len(status_list) % 2 == 1 else 0
    return base
