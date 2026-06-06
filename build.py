#!/usr/bin/env python3
"""Build the personal website from markdown articles."""

import os
import re
import json

ARTICLES_DIR = '/Users/chiryyu/Documents/涉外律师/新文章'
SITE_DIR = '/Users/chiryyu/Documents/涉外律师/website'
ARTICLES_OUT = os.path.join(SITE_DIR, 'articles')

os.makedirs(ARTICLES_OUT, exist_ok=True)

# ===== Article metadata =====
META = {
    '01_泰国税务争议应对.md': {
        'slug': '01-thailand-tax-dispute',
        'region': '泰国', 'tag': '税务合规',
        'date': '2026-06-07',
        'desc': '泰国税务局2025年追缴税款超480亿泰铢，转移定价稽查从18%飙升至35%。本文系统解析从稽查通知到行政诉讼的全流程应对策略，为中资企业提供可落地的防御性合规指引。',
    },
    '02_柬埔寨QIP申请实务.md': {
        'slug': '02-cambodia-qip',
        'region': '柬埔寨', 'tag': '投资法',
        'date': '2026-06-08',
        'desc': '2021年新投资法实现从"正面清单"到"负面清单+激励分级"的根本转变。本文拆解QIP从申请流程、税收优惠规则到持续合规义务的全流程操作要点。',
    },
    '03_泰国刑事拘留权利保护.md': {
        'slug': '03-thailand-criminal-defense',
        'region': '泰国', 'tag': '刑事辩护',
        'date': '2026-06-09',
        'desc': '从传唤到终审的12个关键节点，拘留阶段的六项核心权利，四大常见涉刑类型辩护要点，以及家属应如何提供有效的外部支持。',
    },
    '04_马来西亚PDPA执法风暴.md': {
        'slug': '04-malaysia-pdpa',
        'region': '马来西亚', 'tag': '数据合规',
        'date': '2026-06-10',
        'desc': '2024年PDPA修订后处罚上限提升至100万令吉+3年监禁。本文与GDPR和泰国PDPA横向对比，解析2025-2026年执法趋势与中资企业实操合规路径。',
    },
    '05_罗马尼亚劳动法实务.md': {
        'slug': '05-romania-labor-law',
        'region': '罗马尼亚', 'tag': '劳动法',
        'date': '2026-06-11',
        'desc': '罗马尼亚劳动法受欧盟指令深度影响，对雇员保护远超中国标准。本文详解雇佣、解雇、加班、工会谈判的操作红线和合规要点。',
    },
    '06_柬埔寨建筑施工许可.md': {
        'slug': '06-cambodia-construction',
        'region': '柬埔寨', 'tag': '工程法',
        'date': '2026-06-12',
        'desc': '施工许可不全→工程停工、竣工备案无法通过→无法结算尾款、工程款拖欠→无力整改——恶性循环。本文拆解从三证体系到纠纷救济的全流程。',
    },
    '07_越南数据本地化合规.md': {
        'slug': '07-vietnam-data-localization',
        'region': '越南', 'tag': '数据合规',
        'date': '2026-06-13',
        'desc': '第55号法令2026年生效，越南成为东盟数据本地化最严国家。本文详解触发本地化的"三步审查法"、跨境传输审批机制与中资企业合规进入路径。',
    },
    '08_印尼IKN投资法律框架.md': {
        'slug': '08-indonesia-ikn',
        'region': '印尼', 'tag': '投资法',
        'date': '2026-06-14',
        'desc': 'IKN总投资预估300亿美元，OIKN享有超常规权力。本文解析外资准入的"超国民待遇"、土地征收法律争议与PPP模式的四种架构。',
    },
    '09_泰国工厂法工业用地合规.md': {
        'slug': '09-thailand-factory-act',
        'region': '泰国', 'tag': '行政合规',
        'date': '2026-06-15',
        'desc': 'DIW 2026年启动3类工厂全面合规审查。本文详解从选址的五维审查、EIA审批时间线到排污许可持续达标的工业用地全流程合规要点。',
    },
    '10_东盟六国仲裁执行全景.md': {
        'slug': '10-asean-arbitration',
        'region': '东盟', 'tag': '争议解决',
        'date': '2026-06-16',
        'desc': '东盟六国《纽约公约》覆盖全景比较。从公共政策抗辩到正当程序抗辩，从SIAC到CIETAC的机构选择策略，附仲裁条款设计黄金模板。',
    },
}

# ===== HTML Template =====
HTML_HEAD = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | 余驰宇律师</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{region}法律,{tag},跨境投资,余驰宇律师">
<meta name="author" content="余驰宇">
<link rel="canonical" href="https://chiryyu.com/articles/{slug}.html">
<link rel="stylesheet" href="/css/style.css">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "description": "{desc}",
  "author": {{ "@type": "Person", "name": "余驰宇", "url": "https://chiryyu.com" }},
  "datePublished": "{date}T08:00:00+08:00",
  "dateModified": "{date}T08:00:00+08:00",
  "publisher": {{ "@type": "Person", "name": "余驰宇" }},
  "mainEntityOfPage": {{ "@type": "WebPage", "@id": "https://chiryyu.com/articles/{slug}.html" }}
}}
</script>
</head>
<body>

<header class="site-header">
  <div class="header-inner">
    <a href="/" class="site-title">余驰宇<span>律师</span></a>
    <nav class="site-nav">
      <a href="/">首页</a>
      <a href="/articles/">文章</a>
      <a href="/about.html">关于</a>
    </nav>
  </div>
</header>

<article>
  <header class="article-header">
    <div class="article-region">{region} · {tag}</div>
    <h1>{title}</h1>
    <div class="article-meta">余驰宇 · {date}</div>
  </header>
  <div class="article-body">
{body}
  </div>
</article>

<footer class="site-footer">
  <p>© 2026 余驰宇律师. <a href="/">chiryyu.com</a></p>
  <p style="margin-top:0.5rem;"><a href="/articles/">← 返回文章列表</a></p>
</footer>

</body>
</html>'''


def md_to_html(text):
    """Convert simple markdown to HTML paragraphs."""
    paragraphs = text.split('\n')
    html_parts = []
    in_list = False

    for para in paragraphs:
        para = para.strip()
        if not para:
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            continue

        # Section headers: 一、二、三、 or （一）（二） or 引言/结语
        if re.match(r'^[一二三四五六七八九十]、', para):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            html_parts.append(f'<h2>{para}</h2>')
        elif re.match(r'^（[一二三四五六七八九十]）', para):
            html_parts.append(f'<h3>{para}</h3>')
        elif para in ('引言', '结语', '问题的提出'):
            html_parts.append(f'<h2>{para}</h2>')
        elif para.startswith('- ') or para.startswith('* '):
            if not in_list:
                html_parts.append('<ul>')
                in_list = True
            html_parts.append(f'<li>{para[2:]}</li>')
        elif re.match(r'^\d+\. ', para):
            if not in_list:
                html_parts.append('<ol>')
                in_list = True
            cleaned = re.sub(r'^\d+\. ', '', para)
            html_parts.append(f'<li>{cleaned}</li>')
        else:
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            html_parts.append(f'<p>{para}</p>')

    if in_list:
        html_parts.append('</ul>')

    return '\n'.join(html_parts)


# ===== Generate article pages =====
files = sorted([f for f in os.listdir(ARTICLES_DIR) if f.endswith('.md')])

for f in files:
    meta = META.get(f, {})
    slug = meta.get('slug', f.replace('.md', ''))
    region = meta.get('region', '跨境')
    tag = meta.get('tag', '法律')
    date = meta.get('date', '2026-06-01')
    desc = meta.get('desc', '')

    path = os.path.join(ARTICLES_DIR, f)
    with open(path, 'r', encoding='utf-8') as fh:
        raw = fh.read()

    lines = raw.split('\n')
    title = lines[0].replace('# ', '').strip()
    body_md = '\n'.join(lines[1:])

    # Clean markdown
    body_md = re.sub(r'\*\*(.*?)\*\*', r'\1', body_md)
    body_md = re.sub(r'---', '', body_md)
    body_md = re.sub(r'\|', ' ', body_md)

    html_body = md_to_html(body_md)

    html = HTML_HEAD.format(
        title=title, desc=desc, region=region, tag=tag,
        date=date, slug=slug, body=html_body,
    )

    out_path = os.path.join(ARTICLES_OUT, f'{slug}.html')
    with open(out_path, 'w', encoding='utf-8') as fh:
        fh.write(html)

    print(f'  ✅ {slug}.html')


# ===== Generate articles index =====
article_cards = []
for f in files:
    meta = META.get(f, {})
    slug = meta.get('slug', '')
    region = meta.get('region', '')
    tag = meta.get('tag', '')
    date = meta.get('date', '')
    desc = meta.get('desc', '')

    path = os.path.join(ARTICLES_DIR, f)
    with open(path, 'r', encoding='utf-8') as fh:
        title = fh.readline().replace('# ', '').strip()

    article_cards.append(f'''  <a href="/articles/{slug}.html" class="article-card">
    <div class="card-meta">{region} · {tag}</div>
    <div class="card-title">{title}</div>
    <div class="card-desc">{desc}</div>
  </a>''')

articles_html = '\n'.join(article_cards)

articles_page = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>文章列表 | 余驰宇律师 · 跨境投资法律实务</title>
<meta name="description" content="余驰宇律师的跨境投资法律实务文章合集，覆盖泰国、柬埔寨、马来西亚、罗马尼亚、越南、印尼六国，含税务合规、投资法、刑事辩护、数据合规等主题。">
<link rel="stylesheet" href="/css/style.css">
</head>
<body>

<header class="site-header">
  <div class="header-inner">
    <a href="/" class="site-title">余驰宇<span>律师</span></a>
    <nav class="site-nav">
      <a href="/">首页</a>
      <a href="/articles/" class="active">文章</a>
      <a href="/about.html">关于</a>
    </nav>
  </div>
</header>

<main class="main-content">
  <h2 class="section-title">全部文章（共 {len(files)} 篇）</h2>
{articles_html}
</main>

<footer class="site-footer">
  <p>© 2026 余驰宇律师. <a href="/">chiryyu.com</a></p>
</footer>

</body>
</html>'''

index_path = os.path.join(ARTICLES_OUT, 'index.html')
with open(index_path, 'w', encoding='utf-8') as fh:
    fh.write(articles_page)
print('\n  ✅ articles/index.html')

# ===== About page =====
about_html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>关于 | 余驰宇律师</title>
<meta name="description" content="余驰宇，中国执业律师，专注跨境投资法律实务，牵头泰国、柬埔寨、马来西亚、罗马尼亚等国当地律所的中国业务部。">
<link rel="stylesheet" href="/css/style.css">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "余驰宇",
  "jobTitle": "律师",
  "description": "中国执业律师，专注跨境投资法律实务",
  "url": "https://chiryyu.com",
  "knowsAbout": ["跨境投资法","泰国法律","柬埔寨法律","马来西亚法律","罗马尼亚法律","国际仲裁","税务合规"],
  "address": { "@type": "PostalAddress", "addressLocality": "上海", "addressCountry": "CN" }
}
</script>
</head>
<body>

<header class="site-header">
  <div class="header-inner">
    <a href="/" class="site-title">余驰宇<span>律师</span></a>
    <nav class="site-nav">
      <a href="/">首页</a>
      <a href="/articles/">文章</a>
      <a href="/about.html" class="active">关于</a>
    </nav>
  </div>
</header>

<section class="about-hero">
  <h1>余驰宇</h1>
  <p>中国执业律师 · 跨境投资法律实务</p>
</section>

<main class="about-content">
  <h2>执业领域</h2>
  <p>余驰宇，中国执业律师，牵头泰国、柬埔寨、马来西亚、罗马尼亚等国当地律所的中国业务部，专注中资企业海外财产保护、重大诉讼/仲裁、税务问题处理、跨境保全与执行。</p>

  <h2>覆盖法域</h2>
  <ul>
    <li><strong>泰国</strong> — BOI投资、反洗钱法、公司治理、EPC工程、工作签证、土地法、股权代持</li>
    <li><strong>柬埔寨</strong> — 新投资法QIP、矿业投资、信托制度、商标保护、赌场牌照、银行牌照、法院执行</li>
    <li><strong>马来西亚</strong> — 资产保全执行、特许经营、仲裁第三方资助、土地法、PDPA数据合规、CIPAA工程款、中国仲裁承认与执行</li>
    <li><strong>罗马尼亚</strong> — 民事诉讼制度、储能投资、工业园区、外资审查、可再生能源、公共采购、欧盟国家援助规则</li>
    <li><strong>越南</strong> — 数据本地化、跨境数据传输合规</li>
    <li><strong>印尼</strong> — 新首都IKN投资、外资准入、PPP模式</li>
  </ul>

  <h2>联系方式</h2>
  <p>关注百家号/知乎/微信公众号：余驰宇律师</p>
  <p>网站：<a href="https://chiryyu.com">chiryyu.com</a></p>
</main>

<footer class="site-footer">
  <p>© 2026 余驰宇律师. <a href="/">chiryyu.com</a></p>
</footer>

</body>
</html>'''

about_path = os.path.join(SITE_DIR, 'about.html')
with open(about_path, 'w', encoding='utf-8') as fh:
    fh.write(about_html)
print('  ✅ about.html')

# ===== robots.txt =====
robots = '''User-agent: *
Allow: /
Sitemap: https://chiryyu.com/sitemap.xml

User-agent: GPTBot
Allow: /

User-agent: CCBot
Allow: /

User-agent: anthropic-ai
Allow: /
'''
with open(os.path.join(SITE_DIR, 'robots.txt'), 'w') as fh:
    fh.write(robots)
print('  ✅ robots.txt')

# ===== sitemap.xml =====
urls = ['https://chiryyu.com/', 'https://chiryyu.com/about.html', 'https://chiryyu.com/articles/']
for f in files:
    meta = META.get(f, {})
    slug = meta.get('slug', '')
    date = meta.get('date', '2026-06-01')
    urls.append(f'https://chiryyu.com/articles/{slug}.html')

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in urls:
    sitemap += f'  <url>\n    <loc>{url}</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
sitemap += '</urlset>\n'

with open(os.path.join(SITE_DIR, 'sitemap.xml'), 'w') as fh:
    fh.write(sitemap)
print('  ✅ sitemap.xml')

# ===== CNAME =====
with open(os.path.join(SITE_DIR, 'CNAME'), 'w') as fh:
    fh.write('chiryyu.com')
print('  ✅ CNAME')

print('\n✅ 网站构建完成！')
