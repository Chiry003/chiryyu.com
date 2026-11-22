#!/usr/bin/env python3
"""Generate 6 cover images for articles 106/107/109/112/113/116."""
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
    {"file": "106_cover.png", "title": "Bakong跨境支付2026全景", "subtitle": "银联、支付宝+、微信支付三条通道与中资资金合规边界", "region": "柬埔寨", "tag": "跨境支付"},
    {"file": "107_cover.png", "title": "2027制衣业最低工资212美元", "subtitle": "Prakas 226/26生效，中资工厂成本重算与NSSF合规清单", "region": "柬埔寨", "tag": "劳动法"},
    {"file": "109_cover.png", "title": "泰国跨境电商税务合规实务", "subtitle": "进口7%增值税、平台报送与预提税的落地规则", "region": "泰国", "tag": "税务合规"},
    {"file": "112_cover.png", "title": "马来西亚AMLA 2026执法升级", "subtitle": "Act A1761个人责任、受益所有人新规与中资企业风险清单", "region": "马来西亚", "tag": "刑事合规"},
    {"file": "113_cover.png", "title": "马来西亚2027预算案解读", "subtitle": "GSH 5%税率、外资公司8%印花税与转让定价新规", "region": "马来西亚", "tag": "税务合规"},
    {"file": "116_cover.png", "title": "罗马尼亚2026财税新政", "subtitle": "政局危机落幕后的OUG第8/2026号令与中资税务方案", "region": "罗马尼亚", "tag": "税务合规"},
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
    draw.text((70, 110), f"{art['region']}法律实务 | {art['tag']}", fill=DARK_GOLD, font=font_topic)

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

    title_y = 170
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
