#!/usr/bin/env python3
"""Generate 10 cover images for articles 75-84."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 800, 450
OUTPUT_DIR = '/Users/chiryyu/Documents/涉外律师/website/images'
FONT_TITLE = '/System/Library/Fonts/STHeiti Medium.ttc'
FONT_SUBTITLE = '/System/Library/Fonts/STHeiti Light.ttc'

BG_COLOR = (26, 35, 50)
GOLD = (201, 169, 98)
WHITE = (220, 220, 225)
DARK_GOLD = (160, 130, 65)
ACCENT_BLUE = (60, 100, 160)

ARTICLES = [
    {"file": "75_cover.png", "title": "泰国数字银行与金融科技监管", "subtitle": "虚拟银行牌照、数字资产与电子支付合规全解析", "region": "泰国", "tag": "金融监管"},
    {"file": "76_cover.png", "title": "柬埔寨数据保护法前瞻", "subtitle": "PDPL草案深度解读与中资企业提前合规路线图", "region": "柬埔寨", "tag": "数据合规"},
    {"file": "77_cover.png", "title": "马来西亚可再生能源与氢能经济", "subtitle": "NETR第二阶段2,500亿林吉特清洁能源投资指引", "region": "马来西亚", "tag": "能源法"},
    {"file": "78_cover.png", "title": "罗马尼亚数字服务法与AI法案", "subtitle": "DSA四层义务+AI Act四类风险的2026合规行动清单", "region": "罗马尼亚", "tag": "数字经济"},
    {"file": "79_cover.png", "title": "越南可再生能源与EV投资", "subtitle": "PDP8实施计划+DPPA私人直供+EV电池千亿赛道", "region": "越南", "tag": "能源法"},
    {"file": "80_cover.png", "title": "印尼Halal认证与食品医药监管", "subtitle": "2026年10月强制化大限与3,200亿美元市场的法律门槛", "region": "印尼", "tag": "行业准入"},
    {"file": "81_cover.png", "title": "柬埔寨储能与碳信用法律框架", "subtitle": "太阳能+储能PPA谈判与1.2亿吨碳信用投资新赛道", "region": "柬埔寨", "tag": "能源法"},
    {"file": "82_cover.png", "title": "马来西亚数字银行与加密货币监管", "subtitle": "五张牌照年度回顾与SC 2026年数字资产指引修订", "region": "马来西亚", "tag": "金融监管"},
    {"file": "83_cover.png", "title": "欧盟CBAM碳边境调节机制与东南亚应对", "subtitle": "2026年正式征收，88欧元/tCO2碳价下的六国竞争力对比", "region": "跨境", "tag": "碳合规"},
    {"file": "84_cover.png", "title": "中资出海东盟十维法律尽调手册", "subtitle": "跨境投资律师的实战框架：从三起失败案例到红绿灯系统", "region": "跨境", "tag": "投资法"},
]

for art in ARTICLES:
    img = Image.new('RGB', (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (W, 4)], fill=GOLD)
    draw.rectangle([(40, 60), (46, H - 60)], fill=GOLD)

    try:
        font_tag = ImageFont.truetype(FONT_TITLE, 16)
    except:
        font_tag = ImageFont.load_default()
    tag_text = f"【{art['region']}】"
    tag_bbox = draw.textbbox((0, 0), tag_text, font=font_tag)
    tag_w = tag_bbox[2] - tag_bbox[0]
    tag_x = W - tag_w - 50
    draw.rounded_rectangle([(tag_x - 15, 48), (tag_x + tag_w + 15, 78)], radius=6, fill=ACCENT_BLUE)
    draw.text((tag_x, 50), tag_text, fill=WHITE, font=font_tag)

    try:
        font_topic = ImageFont.truetype(FONT_SUBTITLE, 13)
    except:
        font_topic = font_tag
    draw.text((W - draw.textbbox((0, 0), art['tag'], font=font_topic)[2] - 50, 92), art['tag'], fill=GOLD, font=font_topic)

    try:
        font_title = ImageFont.truetype(FONT_TITLE, 30)
    except:
        font_title = font_tag

    max_title_w = W - 160
    lines = []; current = ""
    for ch in art['title']:
        test = current + ch
        if draw.textbbox((0, 0), test, font=font_title)[2] > max_title_w:
            lines.append(current); current = ch
        else:
            current = test
    lines.append(current)

    title_y = 180
    for line in lines:
        draw.text((70, title_y), line, fill=WHITE, font=font_title)
        title_y += 46

    try:
        font_sub = ImageFont.truetype(FONT_SUBTITLE, 18)
    except:
        font_sub = font_tag
    draw.text((70, title_y + 20), art['subtitle'], fill=DARK_GOLD, font=font_sub)

    draw.rectangle([(40, H - 55), (W - 40, H - 54)], fill=(50, 60, 80))
    try:
        font_brand = ImageFont.truetype(FONT_TITLE, 14)
    except:
        font_brand = font_tag
    draw.text((70, H - 40), "余驰宇律师  |  跨境投资法律实务", fill=(120, 130, 150), font=font_brand)
    draw.rectangle([(W - 60, H - 30), (W - 48, H - 18)], fill=GOLD)
    draw.rectangle([(W - 75, H - 30), (W - 63, H - 18)], fill=(100, 110, 130))

    path = os.path.join(OUTPUT_DIR, art['file'])
    img.save(path, 'PNG')
    print(f"  [OK] {art['file']}")

print(f"\nDone. {len(ARTICLES)} covers generated.")
