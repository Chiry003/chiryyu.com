#!/usr/bin/env python3
"""Generate 10 cover images for articles 95-104 (Cambodia series)."""
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
    {"file": "95_cover.png", "title": "柬埔寨资本利得税全面落地", "subtitle": "Prakas 1130修订下的股权转让与20%税负合规实操", "region": "柬埔寨", "tag": "税务合规"},
    {"file": "96_cover.png", "title": "美柬对等贸易协议签署之后", "subtitle": "19%关税、转运稽查与对美出口合规新秩序", "region": "柬埔寨", "tag": "贸易法"},
    {"file": "97_cover.png", "title": "制造业QIP实际资本三年大限", "subtitle": "CDC第1555号指令下的达标测算与激励保住策略", "region": "柬埔寨", "tag": "投资法"},
    {"file": "98_cover.png", "title": "德崇扶南运河PPP法律框架", "subtitle": "五份核心协议、BOT结构与中资参与的法律路径", "region": "柬埔寨", "tag": "基础设施"},
    {"file": "99_cover.png", "title": "柬埔寨反技术诈骗法时代", "subtitle": "最高终身监禁、赌场网络博彩暂停与企业合规红线", "region": "柬埔寨", "tag": "刑事合规"},
    {"file": "100_cover.png", "title": "NBC加密资产监管新政落地", "subtitle": "5%资本限额、CASP牌照与Bakong之外的合规路径", "region": "柬埔寨", "tag": "金融监管"},
    {"file": "101_cover.png", "title": "2029年LDC毕业倒计时", "subtitle": "EBA优惠退坡、关税上调与中资制造企业应对策略", "region": "柬埔寨", "tag": "贸易法"},
    {"file": "102_cover.png", "title": "柬埔寨太阳能新政红利", "subtitle": "进口税归零、屋顶光伏补偿电价与储能投资窗口", "region": "柬埔寨", "tag": "能源法"},
    {"file": "103_cover.png", "title": "跨境电商增值税合规实务", "subtitle": "简化登记、反向征收、低值包裹与数字服务税前瞻", "region": "柬埔寨", "tag": "税务合规"},
    {"file": "104_cover.png", "title": "Prakas 117企业注册新政", "subtitle": "电子签名、股东背景调查与年度申报合规要点", "region": "柬埔寨", "tag": "公司合规"},
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
    draw.text((70, 110), f"柬埔寨法律实务 | {art['tag']}", fill=DARK_GOLD, font=font_topic)

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
