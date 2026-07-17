#!/usr/bin/env python3
"""Generate 10 cover images for Cambodia articles 55-64."""
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
    {"file": "55_cover.png", "title": "柬埔寨公司设立与治理结构", "subtitle": "中资企业市场进入的法律架构与操作指引", "region": "柬埔寨", "tag": "公司法"},
    {"file": "56_cover.png", "title": "柬埔寨投资争端解决与仲裁", "subtitle": "从合同起草到裁决执行的全流程指引", "region": "柬埔寨", "tag": "争议解决"},
    {"file": "57_cover.png", "title": "柬埔寨能源与电力投资法律实务", "subtitle": "从项目开发到PPA签署的全流程解析", "region": "柬埔寨", "tag": "能源法"},
    {"file": "58_cover.png", "title": "柬埔寨农业投资法律指引", "subtitle": "从土地取得到农产品出口的全链条合规", "region": "柬埔寨", "tag": "农业投资"},
    {"file": "59_cover.png", "title": "柬埔寨旅游与酒店业外商投资", "subtitle": "酒店牌照、赌场监管与中资准入的法律路径", "region": "柬埔寨", "tag": "行业准入"},
    {"file": "60_cover.png", "title": "柬埔寨保险业法律监管框架", "subtitle": "中资保险机构的市场准入与合规运营指引", "region": "柬埔寨", "tag": "金融监管"},
    {"file": "61_cover.png", "title": "柬埔寨反腐败与商业贿赂合规", "subtitle": "中资企业的刑事法律红线与合规体系建设", "region": "柬埔寨", "tag": "刑事合规"},
    {"file": "62_cover.png", "title": "柬埔寨移民法与外籍工作许可", "subtitle": "中国公民在柬合法居留与工作的全流程指引", "region": "柬埔寨", "tag": "移民法"},
    {"file": "63_cover.png", "title": "柬埔寨进出口贸易管制与海关法", "subtitle": "关税筹划、原产地合规与海关稽查应对", "region": "柬埔寨", "tag": "贸易法"},
    {"file": "64_cover.png", "title": "柬埔寨PPP与基础设施投资", "subtitle": "BOT/PPP模式的法律架构与项目融资实务", "region": "柬埔寨", "tag": "基础设施"},
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
