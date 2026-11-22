#!/usr/bin/env python3
"""Regenerate the Cambodia article cards section in cambodia-lawyer.html from build.py META."""
import re
from collections import defaultdict

SITE = '/Users/chiryyu/Documents/涉外律师/website'
ART = '/Users/chiryyu/Documents/涉外律师/新文章'

src = open(f'{SITE}/build.py', encoding='utf-8').read()
pattern = re.compile(r"'(\d+_[^']+\.md)': \{(.*?)\n    \},", re.S)
meta = {}
for m in pattern.finditer(src):
    fname, body = m.group(1), m.group(2)
    d = {}
    d['slug'] = re.search(r"'slug': '([^']+)'", body).group(1)
    d['region'] = re.search(r"'region': '([^']+)'", body).group(1)
    d['tag'] = re.search(r"'tag': '([^']+)'", body).group(1)
    d['date'] = re.search(r"'date': '([^']+)'", body).group(1)
    d['desc'] = re.search(r"'desc': '([^']*)'", body).group(1)
    meta[fname] = d

kh = []
for fname, d in meta.items():
    if d['region'] != '柬埔寨':
        continue
    title = open(f'{ART}/{fname}', encoding='utf-8').readline().replace('# ', '').strip()
    kh.append((fname, d, title))
kh.sort(key=lambda x: int(x[0].split('_')[0]))
count = len(kh)

GROUPS = [
    ('投资法与公司设立', ['投资法', '公司合规', '公司法']),
    ('税务合规', ['税务合规']),
    ('金融、支付与外汇', ['金融监管', '跨境支付', '外汇管理']),
    ('土地与不动产', ['土地法', '房地产']),
    ('劳动法', ['劳动法']),
    ('能源与环保', ['能源法', '环境法']),
    ('工程与基础设施', ['工程法', '基础设施']),
    ('知识产权', ['知识产权']),
    ('数字经济与数据', ['数据合规', '数字经济']),
    ('破产与清算', ['破产法']),
    ('农业与旅游', ['农业投资', '旅游', '行业准入']),
    ('保险', ['保险']),
    ('反腐败', ['反腐败']),
    ('移民与签证', ['移民法']),
    ('贸易与海关', ['贸易法', '海关法']),
    ('争议解决', ['争议解决']),
    ('刑事与合规', ['刑事合规']),
]

def group_of(tag):
    for g, tags in GROUPS:
        if tag in tags:
            return g
    return '其他'

groups = defaultdict(list)
for fname, d, title in kh:
    groups[group_of(d['tag'])].append((d, title))

def card(d, title):
    return f'''    <a href="/articles/{d['slug']}.html" class="article-card">
      <div class="card-meta">{d['region']} · {d['tag']} · {d['date'][:7]}</div>
      <div class="card-title">{title}</div>
      <div class="card-desc">{d['desc']}</div>
    </a>'''

cards = []
for gname, _ in GROUPS + [('其他', [])]:
    if gname not in groups:
        continue
    cards.append(f'    <h3 class="region-heading">{gname}</h3>')
    for d, title in groups[gname]:
        cards.append(card(d, title))

new_section = f'''  <section style="max-width:900px;margin:0 auto;padding:2rem 1rem;">
    <h2 style="text-align:center;margin-bottom:2rem;">柬埔寨投资法律文章 · {count}篇</h2>
    <p style="text-align:center;color:var(--gray-400);margin-bottom:2rem;">以下是余驰宇律师撰写的全部柬埔寨法律深度分析文章，每篇均基于一手法律实务经验与真实案例</p>

''' + '\n'.join(cards) + '\n\n  '

html = open(f'{SITE}/cambodia-lawyer.html', encoding='utf-8').read()

html = re.sub(r'已发布\d+篇柬埔寨投资法律深度分析文章', f'已发布{count}篇柬埔寨投资法律深度分析文章', html)
html = re.sub(r'已发布\d+篇柬埔寨法律深度文章', f'已发布{count}篇柬埔寨法律深度文章', html)
html = re.sub(r'\d+篇柬埔寨法律深度文章', f'{count}篇柬埔寨法律深度文章', html)
html = re.sub(r'\d+篇深度文章', f'{count}篇深度文章', html)
html = re.sub(r'柬埔寨投资法律文章 · \d+篇', f'柬埔寨投资法律文章 · {count}篇', html)

h2_anchor = html.index('<h2 style="text-align:center;margin-bottom:2rem;">柬埔寨投资法律文章')
sec_start = html.rindex('<section', 0, h2_anchor)
end = html.index('<section class="consult-section"')
html = html[:sec_start] + new_section + html[end:]

open(f'{SITE}/cambodia-lawyer.html', 'w', encoding='utf-8').write(html)
print(f'Done: {count} Cambodia cards rendered, section rebuilt.')
