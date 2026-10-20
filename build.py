#!/usr/bin/env python3
"""把 content/*.md 轉成 docs/*.html（純靜態網站，GitHub Pages 從 /docs 發布）。

用法：python3 build.py
需要：pip install markdown
"""
import html
import json
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
CONTENT = ROOT / 'content'
OUT = ROOT / 'docs'

SITE_TITLE = 'VLA × 世界模型 調研'
UPDATED = '2026-10-20'

# (slug, 側欄編號, 標題, 一句話說明)
PAGES = [
    ('index', '', '首頁', '這個網站在講什麼、怎麼讀'),
    ('origins', '01', '起源與歷史', '遇到什麼瓶頸，才發展出 VLA 與世界模型'),
    ('architectures', '02', '主流模型架構', 'VLA 四條路線、世界模型四條路線'),
    ('taxonomy', '03', '流派怎麼分', 'VLA 的三條分類軸、世界模型的四個流派'),
    ('training', '04', '訓練、資料與評估', '怎麼訓練、資料怎麼建、輸入輸出、怎麼用、怎麼評估'),
    ('world-model-roles', '05', '世界模型四類與五種角色', '每類吃什麼、吐什麼，VLA 怎麼用它'),
    ('train-vs-inference', '06', '訓練時 vs 推論時', '世界模型實際出現在哪裡、結構與參數量'),
    ('synthetic-data', '07', '具身基礎模型與合成資料', '「融合」是什麼意思、生成影片怎麼把關物理'),
    ('industry', '08', '業界產品盤點', '機器人與自駕公司各自怎麼做'),
    ('ai2-robotics', '09', '案例：智平方', '產品分類、競品比較、類腦與 SNN'),
    ('glossary', '10', '名詞速查', '常見術語一句話解釋'),
    ('references', '11', '參考資料', '論文、官方頁與本專案原始產出'),
]

MD_EXT = ['tables', 'toc', 'admonition', 'attr_list', 'md_in_html', 'fenced_code', 'sane_lists', 'def_list']
MD_CFG = {'toc': {'permalink': '#', 'permalink_title': '連到此段', 'toc_depth': '2-3'}}


def postprocess(body: str) -> str:
    # 表格外包一層，窄螢幕可橫向捲動
    body = re.sub(r'<table>', '<div class="tbl"><table>', body)
    body = re.sub(r'</table>', '</table></div>', body)
    # 外部連結開新分頁
    body = re.sub(r'<a href="(https?://[^"]+)"',
                  r'<a class="ext" href="\1" target="_blank" rel="noopener"', body)
    return body


def toc_html(tokens) -> str:
    items = []
    for t in tokens:
        sub = ''
        if t.get('children'):
            sub = '<ul>' + ''.join(
                f'<li><a href="#{c["id"]}">{html.escape(c["name"])}</a></li>' for c in t['children']) + '</ul>'
        items.append(f'<li><a href="#{t["id"]}">{html.escape(t["name"])}</a>{sub}</li>')
    return '<ul>' + ''.join(items) + '</ul>' if items else ''


def flat_tokens(tokens):
    # toc_depth 2-3：最上層就是 h2
    out = []
    for t in tokens:
        if t['level'] == 1:
            out.extend(t.get('children', []))
        else:
            out.append(t)
    return out


def nav_html(current: str) -> str:
    rows = []
    for slug, num, title, _ in PAGES:
        cls = ' class="on"' if slug == current else ''
        n = f'<span class="num">{num}</span>' if num else '<span class="num">⌂</span>'
        rows.append(f'<li><a href="{slug}.html"{cls}>{n}<span>{html.escape(title)}</span></a></li>')
    return '<ul class="nav">' + ''.join(rows) + '</ul>'


def strip_tags(frag: str) -> str:
    frag = re.sub(r'>\s+<', '><', frag)
    frag = re.sub(r'<(marker|defs).*?</\1>', ' ', frag, flags=re.S)
    frag = re.sub(r'</text>', ' ', frag)
    frag = re.sub(r'<a class="headerlink".*?</a>', '', frag, flags=re.S)
    frag = re.sub(r'</(p|li|tr|h[1-6]|figcaption|div)>', '\n', frag)
    frag = re.sub(r'</t[dh]>', '｜', frag)
    frag = re.sub(r'<[^>]+>', '', frag)
    frag = html.unescape(frag)
    frag = re.sub(r'[ \t]+', ' ', frag)
    return re.sub(r'\n\s*\n+', '\n', frag).strip()


def sections(slug: str, title: str, body: str):
    """把一頁切成以 h2/h3 為單位的段落，給站內問答檢索用。"""
    parts = re.split(r'(<h[23] id="[^"]+">.*?</h[23]>)', body, flags=re.S)
    out = [{'p': slug, 't': title, 's': title, 'a': '', 'x': strip_tags(parts[0])}]
    for i in range(1, len(parts), 2):
        m = re.match(r'<h[23] id="([^"]+)">(.*?)</h[23]>', parts[i], flags=re.S)
        out.append({'p': slug, 't': title, 's': strip_tags(m.group(2)), 'a': m.group(1),
                    'x': strip_tags(parts[i + 1])})
    if slug == 'glossary':
        # 名詞速查：每一列各自成一筆，問「X 是什麼」時能直接命中
        rows = []
        for o in out:
            for line in o['x'].split('\n'):
                cells = [c.strip() for c in line.split('｜') if c.strip()]
                if len(cells) >= 2 and cells[0] not in ('名詞', '代號'):
                    rows.append({'p': slug, 't': title, 's': cells[0], 'a': o['a'], 'x': '：'.join(cells[:2])})
        return rows
    return [o for o in out if o['x']]


TEMPLATE = (ROOT / 'template.html').read_text(encoding='utf-8')


def build():
    OUT.mkdir(exist_ok=True)
    index = []
    for i, (slug, num, title, desc) in enumerate(PAGES):
        src = (CONTENT / f'{slug}.md').read_text(encoding='utf-8')
        md = markdown.Markdown(extensions=MD_EXT, extension_configs=MD_CFG)
        body = postprocess(md.convert(src))
        if slug != 'references':
            index.extend(sections(slug, title, body))
        toc = toc_html(flat_tokens(md.toc_tokens))
        prev_ = PAGES[i - 1] if i > 0 else None
        next_ = PAGES[i + 1] if i + 1 < len(PAGES) else None
        pn = '<nav class="pn">'
        pn += (f'<a class="prev" href="{prev_[0]}.html"><small>上一篇</small>{html.escape(prev_[2])}</a>'
               if prev_ else '<span></span>')
        pn += (f'<a class="next" href="{next_[0]}.html"><small>下一篇</small>{html.escape(next_[2])}</a>'
               if next_ else '<span></span>')
        pn += '</nav>'
        page_title = SITE_TITLE if slug == 'index' else f'{title} · {SITE_TITLE}'
        out = (TEMPLATE
               .replace('{{PAGE_TITLE}}', html.escape(page_title))
               .replace('{{DESC}}', html.escape(desc))
               .replace('{{SITE_TITLE}}', html.escape(SITE_TITLE))
               .replace('{{NAV}}', nav_html(slug))
               .replace('{{TOC}}', toc)
               .replace('{{BODY}}', body)
               .replace('{{PREVNEXT}}', pn)
               .replace('{{UPDATED}}', UPDATED)
               .replace('{{SLUG}}', slug))
        (OUT / f'{slug}.html').write_text(out, encoding='utf-8')
        print('built', slug)
    (OUT / '.nojekyll').write_text('')
    # 用 .js 而不是 .json：直接開本機檔案（file://）也能載入
    (OUT / 'assets' / 'search-index.js').write_text(
        'window.SITE_INDEX=' + json.dumps(index, ensure_ascii=False, separators=(',', ':')) + ';\n',
        encoding='utf-8')
    print('indexed', len(index), 'sections')


if __name__ == '__main__':
    build()
