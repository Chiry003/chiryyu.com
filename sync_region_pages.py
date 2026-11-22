#!/usr/bin/env python3
"""Regenerate article card sections and count texts for all region lawyer pages from build.py META."""
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

PAGES = [
    ('thailand', ['泰国']),
    ('malaysia', ['马来西亚']),
    ('romania', ['罗马尼亚']),
    ('vietnam', ['越南']),
    ('indonesia', ['印尼']),
    ('crossborder', ['跨境', '东盟']),
]

for page, regions in PAGES:
    arts = []
    for fname, d in meta.items():
        if d['region'] in regions:
            title = open(f'{ART}/{fname}', encoding='utf-8').readline().replace('# ', '').strip()
            arts.append((fname, d, title))
    arts.sort(key=lambda x: int(x[0].split('_')[0]))
    count = len(arts)

    cards = []
    for fname, d, title in arts:
        cards.append(f'''    <a href="/articles/{d['slug']}.html" class="article-card">
      <div class="card-meta">{d['region']} · {d['tag']} · {d['date'][:7]}</div>
      <div class="card-title">{title}</div>
      <div class="card-desc">{d['desc']}</div>
    </a>''')

    html = open(f'{SITE}/{page}-lawyer.html', encoding='utf-8').read()

    h2_anchor = html.index('<h2 style="text-align:center;margin-bottom:2rem;">') if 'margin-bottom:2rem;">' in html else None
    # find the article-list h2 specifically
    m = re.search(r'<h2 style="text-align:center;margin-bottom:2rem;">[^<]*投资法律文章', html)
    if not m:
        print(f'{page}: article h2 not found, skip')
        continue
    h2_idx = m.start()
    sec_start = html.rindex('<section', 0, h2_idx)
    end = html.index('<section class="consult-section"')
    new_h2 = f'<h2 style="text-align:center;margin-bottom:2rem;">{m.group(0).split(">")[-1].split("·")[0].strip()} · {count}篇</h2>'
    new_section = f'  <section style="max-width:900px;margin:0 auto;padding:2rem 1rem;">\n    {new_h2}\n\n' + '\n'.join(cards) + '\n\n  '
    html = html[:sec_start] + new_section + html[end:]

    # update counts in meta tags and stats text
    if page == 'crossborder':
        total_site = len(meta)
        html = re.sub(r'已发布\d+篇深度文章', f'已发布{total_site}篇深度文章', html)
        html = re.sub(r'\d+篇深度文章', f'{total_site}篇深度文章', html)
        html = re.sub(r'\d+篇文章', f'{count}篇文章', html)
    else:
        rname = regions[0]
        html = re.sub(r'已发布\d+篇' + rname + r'法律深度文章', f'已发布{count}篇{rname}法律深度文章', html)
        html = re.sub(r'已发布\d+篇' + rname + r'法律深度分析文章', f'已发布{count}篇{rname}法律深度分析文章', html)
        html = re.sub(r'\d+篇深度文章', f'{count}篇深度文章', html)
        html = re.sub(r'\d+篇' + rname + r'法律深度文章', f'{count}篇{rname}法律深度文章', html)

    open(f'{SITE}/{page}-lawyer.html', 'w', encoding='utf-8').write(html)
    print(f'{page}: {count} cards, counts updated')
