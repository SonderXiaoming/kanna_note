from dataclasses import fields, is_dataclass
from datetime import datetime, timedelta
import re
import string
from typing import Any, AsyncGenerator
import httpx
from pydantic import BaseModel
import zhconv
from hoshino.modules.priconne import chara
from PIL import Image
import io
import base64

phase_dict = {letter: i for i, letter in enumerate(string.ascii_uppercase, start=1)}
phase_dict_reverse = {v: k for k, v in phase_dict.items()}


async def download_stream(
    url: str, chunk_size: int = 1024
) -> AsyncGenerator[bytes, None]:
    async with httpx.AsyncClient(timeout=10) as client:
        async with client.stream("GET", url) as rsp:
            rsp.raise_for_status()
            async for chunk in rsp.aiter_bytes(chunk_size):
                yield chunk  # 逐块返回数据


def get_chara(name):
    if name[0] == "#":
        return int(name[1:]), ""
    id_ = chara.name2id(name)
    confi = 100
    msg = ""
    if id_ == chara.UNKNOWN:
        id_, guess_name, confi = chara.guess_id(name)
    c = chara.fromid(id_)

    if confi < 100:
        msg = f'兰德索尔似乎没有叫"{name}"的人...\n角色别称补全计划: github.com/Ice-Cirno/HoshinoBot/issues/5\n您有{confi}%的可能在找{guess_name}{c.icon.cqcode}'

    return id_, msg


def chara_id2name(id_):
    return chara.fromid(id_).name


def is_text_chinese(text: str) -> bool:
    """判断字符串是否是中文"""
    return bool(re.search(r"[\u4e00-\u9fff]*", text))


def convert2gameid(id_):
    return id_ * 100 + 1


def convert2charid(id_):
    return id_ // 100


def convert2simplified(obj: Any):
    """
    遍历 dataclass 或 pydantic 对象，将所有字符串转换为简体
    """

    def convert(value):
        if isinstance(value, str):
            return zhconv.convert(value, "zh-cn")  # 繁体转简体
        elif isinstance(value, list):
            return [convert(v) for v in value]
        elif isinstance(value, dict):
            return {k: convert(v) for k, v in value.items()}
        elif is_dataclass(value):
            return convert2simplified(value)
        elif isinstance(value, BaseModel):
            return convert2simplified(value)
        return value

    if is_dataclass(obj):
        updated_data = {
            field.name: convert(getattr(obj, field.name)) for field in fields(obj)
        }
        return obj.__class__(**updated_data)
    elif isinstance(obj, BaseModel):
        updated_data = {
            field: convert(getattr(obj, field)) for field in obj.__fields__.keys()
        }
        return obj.__class__(**updated_data)
    else:
        raise TypeError(f"Unsupported type {type(obj)}")


pcr_limit_type_dict = {
    1: "常驻",
    2: "限定",
    3: "活动",
    4: "兑换",
}


def limit_type_int2str(limit_type: int) -> str:
    return pcr_limit_type_dict.get(limit_type, "未知")


def search_type_distance2str(distance: int) -> str:
    return "前卫" if distance < 300 else "后卫" if distance > 600 else "中卫"


def pic2b64(pic: Image.Image) -> str:
    """将 PIL Image 对象转换为 base64 编码的字符串"""

    with io.BytesIO() as bio:
        pic.save(bio, format="PNG")
        return base64.b64encode(bio.getvalue()).decode()


def pic2cqcode(pic: Image.Image) -> str:
    """将 PIL Image 对象转换为 base64 编码的 CQ 码字符串"""

    return f"[CQ:image,file=base64://{pic2b64(pic)}]"


_square_exclude_chars = set(
    string.digits + string.ascii_letters + string.punctuation + string.whitespace
)


def is_square_characters(char: str) -> bool:
    return char not in _square_exclude_chars


def split_text(text: str, max_length: int):
    """
    将输入文本按最大长度拆分成多个部分，其中中文字符计为1个长度，其他字符计为0.5个长度。

    :param text: str，输入的长文本
    :param max_length: int，每部分最大长度（中文字符计为1，其它字符计为0.5）
    :return: list，分割后的文本列表
    """
    if not text or max_length <= 0:
        return []

    result = []
    punctuation = set("，。！？\n,!? 　")  # 定义优先在这些标点处断开
    start = 0
    n = len(text)

    while start < n:
        cum_weight = 0.0  # 已累计的权重
        pos = start  # 当前字符索引
        last_break = None  # 记录最近一次出现标点的位置

        # 累加权重，直到下一个字符加入会超过 max_length
        while pos < n:
            char = text[pos]
            weight = 1.0 if is_square_characters(char) else 0.5
            if cum_weight + weight > max_length:
                break
            cum_weight += weight
            if char in punctuation:
                last_break = pos  # 记录断点位置
            pos += 1

        # 如果还未达到文本末尾，则尽量在标点处断开
        if pos < n and pos != start and last_break is not None and last_break > start:
            split_index = last_break + 1  # 保留断点字符在当前段落内
        else:
            split_index = pos
        # 去除首尾空白后添加到结果列表
        result.append(text[start:split_index].strip())
        start = split_index

    return result


def split_list(lst, n=6):
    """
    将列表按 n 个元素一组分割，最后一组可以少于 n 个元素。
    :param lst: 需要分割的列表
    :param n: 每组的元素个数，默认为6
    :return: 分割后的列表
    """
    return [lst[i : i + n] for i in range(0, len(lst), n)]


def parse_datetime(raw: str, fix_jp_time: bool = True) -> datetime:
    """
    解析字符串为 datetime，支持格式修正和日本时区调整。
    支持 "YYYY-MM-DD", "YYYY/MM/DD", "YYYY-MM-DD HH:MM", 等格式。
    """
    raw = raw.replace("  ", " ").replace("-", "/").strip()
    parts = raw.split(" ")
    ymd = parts[0].split("/")
    hms = ["00", "00", "00"]

    if len(parts) > 1:
        hms = f"{parts[1]}:00:00".split(":")[:3]

    try:
        dt = datetime(
            int(ymd[0]), int(ymd[1]), int(ymd[2]), int(hms[0]), int(hms[1]), int(hms[2])
        )
    except Exception:
        raise ValueError(f"Invalid date format: {raw}")

    if fix_jp_time:
        dt -= timedelta(hours=1)

    return dt


def is_in_progress(
    today: str, start_time: str, end_time: str, fix_jp_time: bool = True
) -> bool:
    now = parse_datetime(today, fix_jp_time=False)
    start = parse_datetime(start_time, fix_jp_time)
    end = parse_datetime(end_time, fix_jp_time)
    return (
        0 < (now - start).total_seconds() < (end - start).total_seconds()
        and 0 < (end - now).total_seconds() < 31536000
    )


def is_coming_soon(today: str, start_time: str, fix_jp_time: bool = True) -> bool:
    now = parse_datetime(today, fix_jp_time=False)
    start = parse_datetime(start_time, fix_jp_time)
    return (start - now).total_seconds() > 0


def cal_damage_by_max_time_return(boss_hp: int, n: int = 1) -> float:
    """
    根据时间和BOSS血量计算伤害
    :param boss_hp: BOSS血量
    :param n: 刀数
    :return: 计算出的伤害值
    """
    return boss_hp / (21 / 90 + n)
