import logging
import random
from typing import Optional, Dict, List, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.character import Character

logger = logging.getLogger(__name__)

# 小鶴雙拼：聲母字母 → 注音符號
XIAOHE_INITIAL_TO_ZHUYIN = {
    "b": "ㄅ", "p": "ㄆ", "m": "ㄇ", "f": "ㄈ",
    "d": "ㄉ", "t": "ㄊ", "n": "ㄋ", "l": "ㄌ",
    "g": "ㄍ", "k": "ㄎ", "h": "ㄏ",
    "j": "ㄐ", "q": "ㄑ", "x": "ㄒ",
    "v": "ㄓ",  # zh
    "i": "ㄔ",  # ch
    "u": "ㄕ",  # sh
    "r": "ㄖ", "z": "ㄗ", "c": "ㄘ", "s": "ㄙ",
}

# 小鶴雙拼：韻母字母 → 注音符號（取最常見的一個）
XIAOHE_FINAL_TO_ZHUYIN = {
    "a": "ㄚ", "o": "ㄛ", "e": "ㄜ",
    "i": "ㄧ", "u": "ㄨ", "v": "ㄩ",
    "q": "ㄧㄡ", "w": "ㄟ", "r": "ㄨㄢ", "t": "ㄩㄝ",
    "y": "ㄨㄣ", "p": "ㄧㄝ", "s": "ㄨㄥ",
    "d": "ㄞ", "f": "ㄣ", "g": "ㄥ", "h": "ㄤ",
    "j": "ㄢ", "k": "ㄧㄥ", "l": "ㄧㄤ",
    "z": "ㄡ", "x": "ㄨㄚ", "c": "ㄠ", "b": "ㄧㄣ",
    "n": "ㄧㄠ", "m": "ㄧㄢ",
}

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
    " ": "ˉ",  # 一聲（陰平）：空白鍵，以 ˉ 顯示
    "6": "ˊ", "3": "ˇ", "4": "ˋ", "7": "˙",
}


def parse_input_code(input_code: str) -> Tuple[List[str], List[str]]:
    """解析 input_code 為 (zhuyin, keys) 陣列對。

    input_code 以空格分隔各鍵，一聲以尾部空格（空白鍵）表示。
    範例：'w 8  ' → keys=['w','8',' '], zhuyin=['ㄊ','ㄚ','ˉ']
    """
    parts = input_code.split(" ")
    keys = [k for k in parts if k]
    # 原始字串尾部有空格（排除換行）代表一聲空白鍵
    if input_code.rstrip("\n\r\t").endswith(" "):
        keys.append(" ")
    zhuyin = [KEY_TO_ZHUYIN.get(k, "") for k in keys]
    return zhuyin, keys


async def get_random_character(db: AsyncSession, input_method: str = "bopomofo") -> Optional[Dict]:
    try:
        result = await db.execute(
            select(Character).where(Character.input_method == input_method)
        )
        characters = result.scalars().all()
        if not characters:
            return None
        char = random.choice(characters)
        if input_method == "shuangpin":
            # 雙拼：keys 為字母碼（用於輸入驗證），zhuyin 轉換為注音符號（用於顯示）
            keys = list(char.input_code)
            initial_key, final_key = char.input_code[0], char.input_code[1]
            initial_zh = XIAOHE_INITIAL_TO_ZHUYIN.get(initial_key, initial_key)
            final_zh = XIAOHE_FINAL_TO_ZHUYIN.get(final_key, final_key)
            zhuyin = [initial_zh, final_zh]
        else:
            zhuyin, keys = parse_input_code(char.input_code)
        return {"id": char.id, "word": char.character, "zhuyin": zhuyin, "keys": keys}
    except Exception as e:
        logger.error(f"Error getting random character: {e}")
        return None
