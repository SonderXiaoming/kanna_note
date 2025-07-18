from io import BytesIO
import os
from .base import FetchUrl, FilePath
import brotli
from .util import download_stream
import httpx


async def update_pcr_database():
    for url, path in zip(
        (FetchUrl.jp_url.value, FetchUrl.tw_url.value, FetchUrl.cn_url.value),
        (FilePath.jp_db.value, FilePath.tw_db.value, FilePath.cn_db.value),
    ):
        decompressor = brotli.Decompressor()
        with open(FilePath.temp_db.value, "wb") as f:
            async for chunk in download_stream(url):
                f.write(decompressor.process(chunk))

        os.replace(FilePath.temp_db.value, path)  # 替换文件


def generate_pcr_fullcard(id_, star):
    return (
        f"{FetchUrl.fullcard_url.value}/{id_}{star}1.webp",
        FilePath.fullcard.value / f"fullcard_unit_{id_}{star}1.png",
    )


async def cache_download(url, save_path):
    temp = BytesIO()
    async for chunk in download_stream(url):
        temp.write(chunk)
    with open(save_path, "wb") as f:  # 写入文件,防止出错
        f.write(temp.getvalue())


async def get_pcr_fullcard(id_):
    url, save_path = generate_pcr_fullcard(id_, 6)
    if save_path.exists():
        return save_path
    try:
        await cache_download(url, save_path)
        return save_path
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            url, save_path = generate_pcr_fullcard(id_, 3)
            if save_path.exists():
                return save_path
            if not save_path.exists():
                try:
                    await cache_download(url, save_path)
                    return save_path
                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 404:
                        raise ValueError(f"暂无id为{id_}的全卡数据") from e


async def get_skill_icon(skill_icon_id):
    url = f"{FetchUrl.skill_icon_url.value}/{skill_icon_id}.webp"
    save_path = FilePath.skill_icon.value / f"{skill_icon_id}.png"
    if save_path.exists():
        return save_path
    try:
        await cache_download(url, save_path)
        return save_path
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise ValueError(f"暂无id为{skill_icon_id}的技能图标") from e


async def get_equipment_icon(equipment_icon_id):
    url = f"{FetchUrl.equipment_url.value}/{equipment_icon_id}.webp"
    save_path = FilePath.equipment.value / f"{equipment_icon_id}.png"
    if save_path.exists():
        return save_path
    try:
        await cache_download(url, save_path)
        return save_path
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise ValueError(f"暂无id为{equipment_icon_id}的装备图标") from e


async def get_enemy_icon(enemy_id):
    url = f"{FetchUrl.enemy_icon_url.value}/{enemy_id}.webp"
    save_path = FilePath.enemy.value / f"{enemy_id}.png"
    if save_path.exists():
        return save_path
    try:
        await cache_download(url, save_path)
        return save_path
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise ValueError(f"暂无id为{enemy_id}的敌人图标") from e


async def get_teaser_icon(teaser_id, type_):
    utl = f"{FetchUrl.teaser_url.value.format(type_)}/{teaser_id}.webp"
    save_path = FilePath.teaser.value / f"{teaser_id}.png"
    if save_path.exists():
        return save_path
    try:
        await cache_download(utl, save_path)
        return save_path
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise ValueError(f"暂无id为{teaser_id}的预告图标") from e
