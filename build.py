#!/usr/bin/env python3
"""Build the personal website from markdown articles."""

import os
import re

ARTICLES_DIR = '/Users/chiryyu/Documents/涉外律师/新文章'
SITE_DIR = '/Users/chiryyu/Documents/涉外律师/website'
ARTICLES_OUT = os.path.join(SITE_DIR, 'articles')

os.makedirs(ARTICLES_OUT, exist_ok=True)

META = {
    '01_泰国税务争议应对.md': {
        'slug': '01-thailand-tax-dispute', 'region': '泰国', 'tag': '税务合规',
        'date': '2026-06-07', 'desc': '泰国税务局2025年追缴税款超480亿泰铢，转移定价稽查飙升至35%。本文系统解析从稽查通知到行政诉讼的全流程应对策略。',
    },
    '02_柬埔寨QIP申请实务.md': {
        'slug': '02-cambodia-qip', 'region': '柬埔寨', 'tag': '投资法',
        'date': '2026-06-08', 'desc': '2021年新投资法从"正面清单"转向"负面清单+激励分级"。本文拆解QIP从申请流程、税收优惠规则到持续合规义务的全流程操作要点。',
    },
    '03_泰国刑事拘留权利保护.md': {
        'slug': '03-thailand-criminal-defense', 'region': '泰国', 'tag': '刑事辩护',
        'date': '2026-06-09', 'desc': '从传唤到终审的12个关键节点，拘留阶段的六项核心权利，四大常见涉刑类型辩护要点，以及家属外部支持指南。',
    },
    '04_马来西亚PDPA执法风暴.md': {
        'slug': '04-malaysia-pdpa', 'region': '马来西亚', 'tag': '数据合规',
        'date': '2026-06-10', 'desc': '2024年PDPA修订后处罚上限提升至100万令吉+3年监禁。与GDPR和泰国PDPA横向对比，解析2025-2026年执法趋势与中资企业实操合规路径。',
    },
    '05_罗马尼亚劳动法实务.md': {
        'slug': '05-romania-labor-law', 'region': '罗马尼亚', 'tag': '劳动法',
        'date': '2026-06-11', 'desc': '罗马尼亚劳动法受欧盟指令深度影响，对雇员保护远超中国标准。详解雇佣、解雇、加班、工会谈判的操作红线和合规要点。',
    },
    '06_柬埔寨建筑施工许可.md': {
        'slug': '06-cambodia-construction', 'region': '柬埔寨', 'tag': '工程法',
        'date': '2026-06-12', 'desc': '施工许可不全→工程停工、竣工备案无法通过→无法结算尾款、工程款拖欠→无力整改。拆解从三证体系到纠纷救济的全流程。',
    },
    '07_越南数据本地化合规.md': {
        'slug': '07-vietnam-data-localization', 'region': '越南', 'tag': '数据合规',
        'date': '2026-06-13', 'desc': '第55号法令2026年生效，越南成为东盟数据本地化最严国家。详解触发本地化的"三步审查法"、跨境传输审批机制与中资企业合规路径。',
    },
    '08_印尼IKN投资法律框架.md': {
        'slug': '08-indonesia-ikn', 'region': '印尼', 'tag': '投资法',
        'date': '2026-06-14', 'desc': 'IKN总投资预估300亿美元，OIKN享有超常规权力。解析外资准入的"超国民待遇"、土地征收法律争议与PPP模式的四种架构。',
    },
    '09_泰国工厂法工业用地合规.md': {
        'slug': '09-thailand-factory-act', 'region': '泰国', 'tag': '行政合规',
        'date': '2026-06-15', 'desc': 'DIW 2026年启动3类工厂全面合规审查。详解从选址五维审查、EIA审批时间线到排污许可持续达标的全流程合规要点。',
    },
    '10_东盟六国仲裁执行全景.md': {
        'slug': '10-asean-arbitration', 'region': '东盟', 'tag': '争议解决',
        'date': '2026-06-16', 'desc': '东盟六国《纽约公约》覆盖全景比较。从公共政策抗辩到正当程序抗辩，从SIAC到CIETAC的机构选择策略，附仲裁条款设计黄金模板。',
    },
}

SKIP_LINES = {'余驰宇', '上海', '律师', '关注', '举报/反馈', '评论', '发表', '作者最新文章',
              '换一换', '扫码下载百度APP', '搜最新资讯、看热门视频', '设为首页',
              '我是余驰宇，中国执业律师', '请关注我，私信交流。'}

def normalize_markdown(text):
    """Normalize markdown: convert ## to 一、style for consistency."""
    # Already in 一、format, just clean up
    text = re.sub(r'^##\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^###\s+', '', text, flags=re.MULTILINE)
    return text

def extract_toc(text):
    """Extract table of contents from article body."""
    toc = []
    for line in text.split('\n'):
        line = line.strip()
        # H2: 一、二、三、... or 引言/结语
        if re.match(r'^[一二三四五六七八九十]、', line):
            toc.append(('h2', line))
        elif line in ('引言', '结语', '问题的提出'):
            toc.append(('h2', line))
        # H3: （一）（二）...
        elif re.match(r'^（[一二三四五六七八九十]）', line):
            toc.append(('h3', line))
    return toc

def generate_toc_html(toc):
    """Generate table of contents HTML."""
    if len(toc) < 3:
        return ''
    html = '<nav class="article-toc"><h2>目录</h2><ol>\n'
    for level, title in toc:
        cls = 'toc-h2' if level == 'h2' else 'toc-h3'
        html += f'  <li class="{cls}"><a href="#{title}">{title}</a></li>\n'
    html += '</ol></nav>\n'
    return html

def md_to_html(text):
    """Convert markdown body to well-formatted HTML."""
    text = normalize_markdown(text)
    lines = text.split('\n')
    html = []
    in_ol = False
    in_ul = False
    seen_titles = set()

    def close_lists():
        nonlocal in_ol, in_ul
        if in_ol:
            html.append('</ol>')
            in_ol = False
        if in_ul:
            html.append('</ul>')
            in_ul = False

    for line in lines:
        line = line.strip()
        if not line:
            close_lists()
            continue

        # Skip metadata lines
        if line in SKIP_LINES:
            continue
        if re.match(r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}', line):
            continue
        if line.startswith('©') or line.startswith('京ICP') or line.startswith('京公网'):
            continue
        if re.match(r'^\d+$', line) and len(line) <= 3:
            continue
        if line.startswith('http') and len(line) < 100:
            continue
        if '百度首页' in line or '余驰宇律师' in line:
            continue
        if len(line) < 5 and not re.match(r'^[一二三四五六七八九十]、', line):
            continue

        # H2 headers: ## or 一、二、三、... or special
        is_h2 = False
        if re.match(r'^[一二三四五六七八九十]、', line):
            is_h2 = True
        elif line in ('引言', '结语', '问题的提出'):
            is_h2 = True
        elif re.match(r'^第[一二三四五六七八九十]步', line):
            is_h2 = True

        if is_h2:
            close_lists()
            anchor = line
            html.append(f'<h2 id="{anchor}">{line}</h2>')
            seen_titles.add(line)
            continue

        # H3 headers: ### or （一）（二）...
        if re.match(r'^（[一二三四五六七八九十]）', line):
            close_lists()
            html.append(f'<h3>{line}</h3>')
            continue

        # Bold inline
        line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)

        # Numbered list
        if re.match(r'^\d+[\.\、]', line):
            if not in_ol:
                close_lists()
                html.append('<ol>')
                in_ol = True
            cleaned = re.sub(r'^\d+[\.\、]\s*', '', line)
            html.append(f'<li>{cleaned}</li>')
            continue

        # Bullet list
        if line.startswith('- ') or line.startswith('* '):
            if not in_ul:
                close_lists()
                html.append('<ul>')
                in_ul = True
            html.append(f'<li>{line[2:]}</li>')
            continue

        # Regular paragraph
        close_lists()
        html.append(f'<p>{line}</p>')

    close_lists()
    return '\n'.join(html)


# ===== HTML Templates =====
HTML_ARTICLE = '''<!DOCTYPE html>
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
{toc}
{body}
  </div>
</article>

<footer class="site-footer">
  <p>© 2026 余驰宇律师 · <a href="/">chiryyu.com</a></p>
  <p style="margin-top:0.5rem;">📞 <a href="tel:+8615201911206">15201911206</a> · 微信 chiry003</p>
  <p style="margin-top:0.3rem;"><a href="/articles/">← 返回文章列表</a></p>
</footer>

</body>
</html>'''


# ===== Build =====
files = sorted([f for f in os.listdir(ARTICLES_DIR) if f.endswith('.md')])

for f in files:
    meta = META.get(f, {})
    slug = meta.get('slug', '')
    region = meta.get('region', '跨境')
    tag = meta.get('tag', '法律')
    date = meta.get('date', '')
    desc = meta.get('desc', '')

    path = os.path.join(ARTICLES_DIR, f)
    with open(path, 'r', encoding='utf-8') as fh:
        raw = fh.read()

    lines = raw.split('\n')
    title = lines[0].replace('# ', '').strip()
    body_md = '\n'.join(lines[1:])

    # Clean: remove horizontal rules, table pipes, then normalize
    body_md = re.sub(r'^---\s*$', '', body_md, flags=re.MULTILINE)
    body_md = re.sub(r'\|', ' ', body_md)

    body_normalized = normalize_markdown(body_md)
    toc = extract_toc(body_normalized)
    toc_html = generate_toc_html(toc)
    body_html = md_to_html(body_md)

    html = HTML_ARTICLE.format(
        title=title, desc=desc, region=region, tag=tag,
        date=date, slug=slug, toc=toc_html, body=body_html,
    )

    out_path = os.path.join(ARTICLES_OUT, f'{slug}.html')
    with open(out_path, 'w', encoding='utf-8') as fh:
        fh.write(html)
    print(f'  ✅ {slug}.html')


# ===== Articles Index =====
cards = []
for f in files:
    meta = META.get(f, {})
    slug = meta.get('slug', '')
    region = meta.get('region', '')
    tag = meta.get('tag', '')
    desc = meta.get('desc', '')
    path = os.path.join(ARTICLES_DIR, f)
    with open(path, 'r', encoding='utf-8') as fh:
        title = fh.readline().replace('# ', '').strip()
    cards.append(f'''    <a href="/articles/{slug}.html" class="article-card">
      <div class="card-meta">{region} · {tag}</div>
      <div class="card-title">{title}</div>
      <div class="card-desc">{desc}</div>
    </a>''')

with open(os.path.join(ARTICLES_OUT, 'index.html'), 'w', encoding='utf-8') as fh:
    fh.write(f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>文章列表 | 余驰宇律师</title>
<meta name="description" content="余驰宇律师跨境投资法律实务文章合集，覆盖泰柬马罗越印六国。">
<link rel="stylesheet" href="/css/style.css">
</head>
<body>
<header class="site-header">
  <div class="header-inner">
    <a href="/" class="site-title">余驰宇<span>律师</span></a>
    <nav class="site-nav"><a href="/">首页</a><a href="/articles/" class="active">文章</a><a href="/about.html">关于</a></nav>
  </div>
</header>
<main class="main-content">
  <h2 class="section-title">全部文章（共 {len(files)} 篇）</h2>
{chr(10).join(cards)}
</main>
<footer class="site-footer">
  <p>© 2026 余驰宇律师 · <a href="/">chiryyu.com</a></p>
  <p style="margin-top:0.5rem;">📞 <a href="tel:+8615201911206">15201911206</a> · 微信 chiry003</p>
</footer>
</body>
</html>''')
print('  ✅ articles/index.html')

# ===== About page =====
with open(os.path.join(SITE_DIR, 'about.html'), 'w', encoding='utf-8') as fh:
    fh.write('''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>关于 | 余驰宇律师</title>
<meta name="description" content="余驰宇，中国执业律师，专注跨境投资法律实务。">
<link rel="stylesheet" href="/css/style.css">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "余驰宇", "jobTitle": "律师",
  "description": "中国执业律师，专注跨境投资法律实务",
  "url": "https://chiryyu.com", "telephone": "+8615201911206",
  "knowsAbout": ["跨境投资法","泰国法律","柬埔寨法律","马来西亚法律","罗马尼亚法律","国际仲裁","税务合规"],
  "address": {"@type":"PostalAddress","addressLocality":"上海","addressCountry":"CN"}
}
</script>
</head>
<body>
<header class="site-header">
  <div class="header-inner">
    <a href="/" class="site-title">余驰宇<span>律师</span></a>
    <nav class="site-nav"><a href="/">首页</a><a href="/articles/">文章</a><a href="/about.html" class="active">关于</a></nav>
  </div>
</header>
<section class="about-hero"><h1>余驰宇</h1><p>中国执业律师 · 跨境投资法律实务</p></section>
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
  <p>📞 电话：<a href="tel:+8615201911206">15201911206</a></p>
  <p>💬 微信：<strong>chiry003</strong></p>
  <p>网站：<a href="https://chiryyu.com">chiryyu.com</a></p>
</main>
<footer class="site-footer">
  <p>© 2026 余驰宇律师 · <a href="/">chiryyu.com</a></p>
  <p style="margin-top:0.5rem;">📞 <a href="tel:+8615201911206">15201911206</a> · 微信 chiry003</p>
</footer>
</body>
</html>''')
print('  ✅ about.html')

# ===== robots.txt =====
with open(os.path.join(SITE_DIR, 'robots.txt'), 'w') as fh:
    fh.write('''User-agent: *
Allow: /
Sitemap: https://chiryyu.com/sitemap.xml
User-agent: GPTBot
Allow: /
User-agent: anthropic-ai
Allow: /
''')
print('  ✅ robots.txt')

# ===== sitemap.xml =====
urls = ['https://chiryyu.com/', 'https://chiryyu.com/about.html', 'https://chiryyu.com/articles/']
for f in files:
    meta = META.get(f, {})
    urls.append(f"https://chiryyu.com/articles/{meta.get('slug', '')}.html")

with open(os.path.join(SITE_DIR, 'sitemap.xml'), 'w') as fh:
    fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for url in urls:
        fh.write(f'  <url><loc>{url}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>\n')
    fh.write('</urlset>\n')
print('  ✅ sitemap.xml')

# ===== CNAME =====
with open(os.path.join(SITE_DIR, 'CNAME'), 'w') as fh:
    fh.write('chiryyu.com')

print('\n✅ 网站重建完成！')
