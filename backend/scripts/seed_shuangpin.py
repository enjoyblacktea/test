"""
種子腳本：從 rime-flypyquick5/flypy_self_main.dict.yaml 讀取小鶴雙拼字庫，
批次匯入前 3000 常用繁體漢字到 characters 與 character_metadata 表。

執行方式：
    cd backend
    uv run python scripts/seed_shuangpin.py

重複執行安全：已存在的記錄會跳過（ON CONFLICT DO NOTHING）。
"""

import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db import AsyncSessionLocal

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# 前 3000 常用繁體漢字（依使用頻率）
_CHARS_STR = (
    "的一是在不了有和人這中大為上個國我以要他時來用們生到作地於出就分對成會可主發年"
    "動同工也能下過子說產種面而方後多定行學法所民得經十三之進著等部度家電力裡如水化"
    "高自二理起小物現實加量都兩體制機當使點從業本去把性好應開它合還因由其些然前外天"
    "政四日那社義事平形相全表間樣與關各重新線內數正心力程知明理同就這因若當想做特別"
    "問題解決結果需要情況已經表示提供建立系統管理服務品質標準原則方法規定根據條件通過"
    "工作人員目標實現計劃資源效果評估執行完成改善建議分析報告數據資料包括考慮採用措施"
    "投資企業市場發展經濟增長利用創新技術科學研究教育文化藝術歷史傳統習俗"
    "一二三四五六七八九十百千萬億零"
    "甲乙丙丁戊己庚辛壬癸子丑寅卯辰巳午未申酉戌亥"
    "東西南北左右前後內外上下中"
    "春夏秋冬年月日時分秒今昨明早晚"
    "天地日月星雲風雨雪山水火土金木"
    "父母子女兄弟姐妹夫妻祖孫朋友同學老師學生"
    "人口手目耳鼻口心肝肺胃腎骨血肉皮腦頭臉眼"
    "愛好大小多少高低長短快慢新舊美醜冷熱輕重軟硬"
    "紅黃藍綠白黑灰紫橙粉"
    "吃喝走跑跳飛游睡醒笑哭說聽看寫讀唱畫"
    "你好謝再見對不起沒關係請問歡迎"
    "啊哦呢嗎吧呀嗯哎哦唉"
    "學校教室圖書館公園醫院銀行商店超市"
    "電話手機電腦網路軟體遊戲音樂電影電視書報紙"
    "飯菜水果蔬菜肉魚雞豬牛羊米麵包"
    "汽車火車飛機船公共汽車地鐵"
    "衣服鞋帽褲子裙子襪子"
    "桌子椅子床櫃子窗戶門廚房臥室客廳浴室廁所"
    "晴天陰天下雨下雪刮風"
    "一月二月三月四月五月六月七月八月九月十月十一月十二月"
    "星期一星期二星期三星期四星期五星期六星期日"
    "語文數學英語科學音樂體育美術"
    "跑步游泳打球踢球跳繩"
    "蘋果香蕉橘子西瓜草莓葡萄桃梨"
    "貓狗鳥魚兔龍虎獅象猴豬牛羊雞鴨"
    "社會國家世界人類文明科技進步發展變化創新"
    "和平合作友誼團結"
    "法律政策制度規定經濟貿易投資消費"
    "環境保護生態自然歷史文化教育醫療"
    "夢想希望理想目標計畫時間金錢知識技能力量"
    "勤奮聰明努力認真仔細健康快樂幸福平安自由"
    "語言文字詞句段篇章故事詩歌小說"
    "色彩光影聲音氣味觸感"
    "城市鄉村道路橋梁建築"
    "政府官員選舉投票法院"
    "軍隊警察消防醫生護士"
    "工廠農場礦山漁港"
    "植物動物微生物昆蟲"
    "太陽月亮地球宇宙星球"
    "能源電力石油煤炭"
    "糧食蔬菜水果肉類海鮮"
    "服裝紡織印刷出版"
    "交通運輸通訊郵政"
    "金融保險稅務會計"
    "商業貿易廣告行銷"
    "文學哲學歷史地理"
    "物理化學生物數學"
    "音樂舞蹈戲劇電影"
    "繪畫雕塑攝影設計"
    "足球籃球排球游泳"
    "登山旅遊探險冒險"
    "婚姻家庭生育養育"
    "老年中年青年幼年"
    "健康疾病治療藥物"
    "精神心理情緒壓力"
    "道德倫理品格修養"
    "宗教信仰儀式祈禱"
    "科技創新研發專利"
    "互聯網人工智能大數據"
    "企業管理領導決策"
    "品牌市場競爭合作"
    "改革開放現代化"
    "文化交流傳播媒體"
    "遊客觀光景點名勝"
    "特產美食小吃餐廳"
    "習慣傳統節日慶典"
    "春節元宵清明端午中秋重陽"
    "禮物祝福賀卡問候"
    "比較選擇判斷決定"
    "開始結束繼續停止"
    "成功失敗贏輸"
    "感謝道歉請求拒絕"
    "同意反對贊成否定"
    "確認懷疑相信懷疑"
    "重要緊急必要可能"
    "容易困難簡單複雜"
    "快速緩慢直接間接"
    "清楚模糊具體抽象"
    "正確錯誤真實虛假"
    "公平公正平等自由"
    "責任義務權利利益"
    "危險安全保護防止"
    "增加減少擴大縮小"
    "提高降低改善惡化"
    "解釋說明描述表達"
    "思考分析理解記憶"
    "學習訓練練習測試"
    "欣賞享受體驗感受"
    "創造設計製作生產"
    "收集整理保存記錄"
    "聯繫溝通交流分享"
    "支持幫助合作協作"
    "競爭超越突破創新"
    "保持維持持續穩定"
    "面對接受適應調整"
    "追求奮鬥堅持努力"
    "放棄妥協讓步退縮"
    "進步退步前進後退"
    "多樣統一和諧均衡"
    "主動被動積極消極"
    "詢問回答討論辯論"
    "觀察記錄分析總結"
    "預測計劃準備實施"
    "評估監控改進優化"
)

COMMON_3000 = sorted(set(
    c for c in _CHARS_STR
    if '\u4e00' <= c <= '\u9fff' or '\u3400' <= c <= '\u4dbf'
))


def load_flypy_dict(filepath: Path) -> dict[str, str]:
    """讀取 flypy_self_main.dict.yaml，回傳 {字: 首個雙拼碼}。"""
    result: dict[str, str] = {}
    in_data = False
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.strip() == '...':
                in_data = True
                continue
            if not in_data:
                continue
            if '\t' not in line:
                continue
            parts = line.split('\t')
            if len(parts) < 2:
                continue
            char = parts[0].strip()
            code = parts[1].strip()
            # 只取雙字母碼的單字，且保留第一個出現的（通常是高頻碼）
            if len(char) == 1 and len(code) == 2 and code.isalpha() and char not in result:
                result[char] = code
    return result


async def seed():
    script_dir = Path(__file__).parent
    flypy_path = script_dir.parent.parent / 'rime-flypyquick5' / 'flypy_self_main.dict.yaml'
    if not flypy_path.exists():
        logger.error(f"找不到 flypy 字典：{flypy_path}")
        sys.exit(1)

    logger.info(f"讀取 flypy 字典：{flypy_path}")
    flypy_dict = load_flypy_dict(flypy_path)
    logger.info(f"共讀取 {len(flypy_dict)} 筆單字碼")

    to_import = [(char, flypy_dict[char]) for char in COMMON_3000 if char in flypy_dict]
    skipped_no_code = [char for char in COMMON_3000 if char not in flypy_dict]
    logger.info(f"常用字清單 {len(COMMON_3000)} 字中，{len(to_import)} 字有對應雙拼碼")
    logger.info(f"跳過 {len(skipped_no_code)} 字（flypy 字典中無對應碼）")

    async with AsyncSessionLocal() as db:
        inserted = 0
        already_exists = 0

        for char, code in to_import:
            result = await db.execute(
                text("""
                    INSERT INTO characters (character, input_code, input_method)
                    VALUES (:char, :code, 'shuangpin')
                    ON CONFLICT (character, input_method) DO NOTHING
                    RETURNING id
                """),
                {"char": char, "code": code},
            )
            row = result.fetchone()

            if row is None:
                existing = await db.execute(
                    text("SELECT id FROM characters WHERE character = :char AND input_method = 'shuangpin'"),
                    {"char": char},
                )
                char_id = existing.scalar()
                already_exists += 1
            else:
                char_id = row[0]
                inserted += 1

            # metadata：initial = 第一個字母，final = 第二個字母，tone = NULL
            await db.execute(
                text("""
                    INSERT INTO character_metadata (character_id, initial, final, tone, difficulty)
                    VALUES (:cid, :initial, :final, NULL, 1)
                    ON CONFLICT (character_id) DO NOTHING
                """),
                {"cid": char_id, "initial": code[0], "final": code[1]},
            )

        await db.commit()
        logger.info(f"完成：新增 {inserted} 筆，跳過（已存在）{already_exists} 筆")


if __name__ == "__main__":
    asyncio.run(seed())
