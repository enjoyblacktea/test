"""
初始化腳本：從 characters.input_code 解析注音成分，批次填入 character_metadata。

執行方式：
    cd backend
    uv run python scripts/seed_character_metadata.py

重複執行安全：已存在的記錄會跳過（不覆蓋）。
"""

import asyncio
import logging
import sys
from pathlib import Path

# 確保能 import app 模組
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select, text
from app.db import AsyncSessionLocal

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# 21 個聲母
INITIALS = set("ㄅㄆㄇㄈㄉㄊㄋㄌㄍㄎㄏㄐㄑㄒㄓㄔㄕㄖㄗㄘㄙ")

# 聲調符號 → 數字（無調號 = 1）
TONE_MAP = {"ˉ": 1, "ˊ": 2, "ˇ": 3, "ˋ": 4, "˙": 5}

# KEY_TO_ZHUYIN 對應（從 character_service.py 複製）
KEY_TO_ZHUYIN = {
    "1": "ㄅ", "q": "ㄆ", "a": "ㄇ", "z": "ㄈ",
    "2": "ㄉ", "w": "ㄊ", "s": "ㄋ", "x": "ㄌ",
    "e": "ㄍ", "d": "ㄎ", "c": "ㄏ",
    "r": "ㄐ", "f": "ㄑ", "v": "ㄒ",
    "5": "ㄓ", "t": "ㄔ", "g": "ㄕ", "b": "ㄖ",
    "y": "ㄗ", "h": "ㄘ", "n": "ㄙ",
    "u": "ㄧ", "j": "ㄨ", "m": "ㄩ",
    "8": "ㄚ", "i": "ㄛ", "k": "ㄜ", ",": "ㄝ",
    "9": "ㄞ", "o": "ㄟ", "l": "ㄠ", ".": "ㄡ",
    "0": "ㄢ", "p": "ㄣ", ";": "ㄤ", "/": "ㄥ",
    "-": "ㄦ",
    " ": "ˉ",
    "6": "ˊ", "3": "ˇ", "4": "ˋ", "7": "˙",
}


def parse_zhuyin(input_code: str) -> tuple[str | None, str | None, int | None]:
    """從 input_code 解析 (initial, final, tone)。

    input_code 格式：鍵盤按鍵以空格分隔，尾部空格代表一聲（ˉ）。
    回傳 (initial, final, tone)，initial 可為 None（純韻母字）。
    """
    parts = input_code.split(" ")
    keys = [k for k in parts if k]
    if input_code.rstrip("\n\r\t").endswith(" "):
        keys.append(" ")

    zhuyin = [KEY_TO_ZHUYIN.get(k) for k in keys]

    # 過濾 None（未知按鍵）
    if None in zhuyin:
        return None, None, None

    initial = None
    final_parts = []
    tone = 1  # 預設一聲

    for sym in zhuyin:
        if sym in TONE_MAP:
            tone = TONE_MAP[sym]
        elif sym in INITIALS and initial is None and not final_parts:
            initial = sym
        else:
            final_parts.append(sym)

    final = "".join(final_parts) if final_parts else None

    return initial, final, tone


async def seed():
    async with AsyncSessionLocal() as db:
        # 取所有字符
        result = await db.execute(text("SELECT id, input_code FROM characters"))
        characters = result.fetchall()
        logger.info(f"共 {len(characters)} 筆字符")

        # 取已存在的 character_metadata
        existing = await db.execute(text("SELECT character_id FROM character_metadata"))
        existing_ids = {row[0] for row in existing.fetchall()}
        logger.info(f"已存在 {len(existing_ids)} 筆 metadata，將跳過")

        inserted = 0
        skipped = 0
        unrecognized = 0

        for char_id, input_code in characters:
            if char_id in existing_ids:
                skipped += 1
                continue

            initial, final, tone = parse_zhuyin(input_code)

            if initial is None and final is None and tone is None:
                logger.warning(f"無法解析 character_id={char_id}, input_code={repr(input_code)}")
                unrecognized += 1
                # 仍插入，帶 NULL 值
                tone = None

            await db.execute(
                text(
                    "INSERT INTO character_metadata (character_id, initial, final, tone, difficulty, frequency_rank) "
                    "VALUES (:cid, :initial, :final, :tone, :difficulty, :freq)"
                ),
                {
                    "cid": char_id,
                    "initial": initial,
                    "final": final,
                    "tone": tone,
                    "difficulty": 1,
                    "freq": None,
                },
            )
            inserted += 1

        await db.commit()
        logger.info(f"完成：插入 {inserted} 筆，跳過 {skipped} 筆，無法解析 {unrecognized} 筆")


if __name__ == "__main__":
    asyncio.run(seed())
