import asyncio
import os
import sqlite3
from io import BytesIO
from pathlib import Path

import httpx

from .base import FetchUrl, FilePath
from .database import cn_data, jp_data, tw_data
from .util import download_stream


def validate_sqlite_database(path: Path):
    with open(path, "rb") as f:
        if f.read(16) != b"SQLite format 3\x00":
            raise ValueError(f"下载内容不是 SQLite 数据库: {path}")

    with sqlite3.connect(path) as conn:
        result = conn.execute("PRAGMA quick_check").fetchone()
    if not result or result[0] != "ok":
        raise ValueError(f"SQLite 数据库校验失败: {path}")


async def download_database(url: str, temp_path: Path):
    try:
        import brotli
    except ImportError as e:
        raise RuntimeError(
            "下载 Brotli 压缩数据库需要安装 Brotli: pip install Brotli"
        ) from e

    decompressor = brotli.Decompressor()
    with open(temp_path, "wb") as f:
        async for chunk in download_stream(
            url, chunk_size=64 * 1024, timeout=60, follow_redirects=True
        ):
            f.write(decompressor.process(chunk))
    if not decompressor.is_finished():
        raise ValueError("Brotli 数据库压缩流不完整")
    await asyncio.to_thread(validate_sqlite_database, temp_path)


async def update_pcr_database():
    databases = (
        (FetchUrl.jp_url.value, FilePath.jp_db.value, jp_data),
        (FetchUrl.tw_url.value, FilePath.tw_db.value, tw_data),
        (FetchUrl.cn_url.value, FilePath.cn_db.value, cn_data),
    )
    downloaded = []
    try:
        for url, path, _ in databases:
            temp_path = path.with_name(f"temp_{path.name}")
            downloaded.append((temp_path, path))
            await download_database(url, temp_path)

        for _, _, data in databases:
            await data.engine.dispose()
        for temp_path, path in downloaded:
            os.replace(temp_path, path)
    finally:
        for temp_path, _ in downloaded:
            temp_path.unlink(missing_ok=True)


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
            return FilePath.icon.value / "kailu.png"  # 默认图标


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
