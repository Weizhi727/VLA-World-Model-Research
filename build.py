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

import params_lib

ROOT = Path(__file__).parent
CONTENT = ROOT / 'content'
OUT = ROOT / 'docs'

SITE_TITLE = 'VLA × 世界模型 調研'
UPDATED = '2026-10-22'

# 側欄分組：(分組名稱, [(slug, 標題, 一句話說明, 首頁卡片說明), ...])
# 編號依這裡的順序自動產生；文中 [NN 標題](slug.html) 與 [NN](slug.html) 的 NN 也會在建置時改成最新編號。
GROUPS = [
    ('', [
        ('index', '首頁', '這個網站在講什麼、怎麼讀', ''),
    ]),
    ('入門總覽', [
        ('origins', '起源與歷史', '遇到什麼瓶頸，才發展出 VLA 與世界模型',
         '機器人學與強化學習各自卡在哪裡，以及兩條路線怎麼在 2025 年匯流。'),
        ('training', '訓練、資料與評估', 'VLA 與世界模型並排：怎麼訓練、資料怎麼建、輸入輸出、怎麼用、怎麼評估',
         '四階段訓練、資料金字塔、一條軌跡長什麼樣、閉環部署、真機與模擬評估；每題都把 VLA 與世界模型並排對照。'),
    ]),
    ('VLA', [
        ('vla-architectures', 'VLA 主流架構', '離散 token、連續動作專家、雙系統、預測式 VLA',
         '四條路線的資料流、代表模型比較表，以及 2026 年的收斂趨勢與動手建議。'),
        ('vla-taxonomy', 'VLA 流派怎麼分', '系統架構、動作解碼、中間表徵三條軸與兩軸地圖',
         '「端到端 vs 分層」只是其中一條軸。三篇 VLA 綜述的切法，與建議的兩軸地圖。'),
        ('in-context-imitation', '情境內模仿學習', '給幾條示範就會做新任務、不更新權重：ICRT、Instant Policy、RICL、Skild S1',
         '要解決什麼、四條技術路線、10 篇論文的資料→模型→輸出流程圖、和 VLA 的關係、誰在做。'),
    ]),
    ('世界模型', [
        ('wm-architectures', '世界模型路線與流派', '影片生成、潛空間動力學、JEPA、3D 四大類',
         '四大類各在哪個空間預測未來、代表作、長處與代價，以及綜述用的其他切法。'),
        ('classic-world-models', '經典世界模型論文精讀', 'World Models、MuZero、DreamerV3、GAIA-1、UniSim、Genie、Cosmos、V-JEPA 2',
         '8 篇論文逐篇拆解：背景、問題、方法、架構、資料集、評估指標與局限。'),
    ]),
    ('綜合應用：VLA × 世界模型', [
        ('world-model-roles', '世界模型四類與五種角色', '每類吃什麼、吐什麼，VLA 怎麼用它',
         '每類的輸入輸出與用途；DreamGen、GR-2、VPP、WMPO、UniPi、Veo 評測。'),
        ('train-vs-inference', '訓練時 vs 推論時', '世界模型實際出現在哪裡、怎麼跟 VLA 接線、數據量與參數量',
         'T1–T4 與 I0–I3 各一張流程圖與連動卡：輸入輸出、世界模型的角色、數據量、參數量。'),
        ('synthetic-data', '具身基礎模型與合成資料', '「融合」是什麼意思、生成影片怎麼把關物理',
         '「機器人版 GPT」指什麼；生成影片的物理問題與四層把關。'),
        ('wm-in-practice', '世界模型代表作的實際應用', 'Cosmos、Wan、Veo、Genie、Dreamer、V-JEPA 被誰用；智平方、Helix、GR00T、GR-2 怎麼用',
         '四類代表作各被誰用、用在哪個階段；智平方 AlphaBrain、Helix、GR00T N1／N1.5、GR-2／GR-3 逐一核對。'),
        ('industry', '業界產品盤點', '機器人與自駕公司各自怎麼做',
         'π、Gemini Robotics、GR00T＋Cosmos、Figure、1X、Tesla、Waymo、華為、小鵬等。'),
        ('ai2-robotics', '案例：智平方', '產品分類、競品比較、類腦與 SNN',
         'GOVLA、FiS-VLA、Video2Act、NeuroVLA；與 π0、Helix、GR00T 比較；類腦與 SNN。'),
        ('tesla', '案例：Tesla', 'FSD、Optimus 與神經世界模擬器：用了什麼、多大、資料從哪來、怎麼接',
         'Policy NN 與 World Sim NN 的閉環；FSD v12–V15、Optimus 的參數量、車隊資料、Cortex 算力。'),
    ]),
    ('查詢工具', [
        ('params', '參數量總表', '所有出現過的 VLA 與世界模型，官方公布的參數量',
         '約 110 個 VLA 與世界模型，只列官方公布的參數量與組成，附來源。'),
        ('glossary', '名詞速查', '常見術語一句話解釋',
         'action chunk、flow matching、IDM、RSSM、JEPA、FVD……一句話解釋。'),
        ('references', '參考資料', '論文、官方頁與本專案原始產出',
         '依主題整理的論文清單，以及本專案的原始報告與簡報。'),
    ]),
]

# (slug, 側欄編號, 標題, 一句話說明, 分組, 卡片說明)
PAGES = []
for _g, _items in GROUPS:
    for _slug, _title, _desc, _card in _items:
        _num = f'{len(PAGES):02d}' if PAGES else ''
        PAGES.append((_slug, _num, _title, _desc, _g, _card))
NUM = {p[0]: p[1] for p in PAGES}

# 拆頁後的舊網址：轉到新頁（依錨點決定去 VLA 還是世界模型那頁）
REDIRECTS = {
    'architectures': ('vla-architectures', 'wm-architectures', ['rl', 'jepa', '3d', '_1', '_2', '_3']),
    'taxonomy': ('vla-taxonomy', 'wm-architectures', ['_6']),
}

MD_EXT = ['tables', 'toc', 'admonition', 'attr_list', 'md_in_html', 'fenced_code', 'sane_lists', 'def_list']
MD_CFG = {'toc': {'permalink': '#', 'permalink_title': '連到此段', 'toc_depth': '2-3'}}


def renumber(body: str) -> str:
    """站內連結文字開頭的章節編號一律換成目前的編號，重排章節時不必手改。"""
    def sub(m):
        slug = m.group(2)
        if slug not in NUM or not NUM[slug]:
            return m.group(0)
        return m.group(1) + NUM[slug] + m.group(4)
    return re.sub(r'(<a href="([a-z0-9-]+)\.html(?:#[^"]*)?">)(\d\d)(\s|</a>)', sub, body)


def postprocess(body: str) -> str:
    body = renumber(body)
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
    group = None
    for slug, num, title, _, g, _c in PAGES:
        if g != group:
            group = g
            if g:
                rows.append(f'<li class="grp">{html.escape(g)}</li>')
        cls = ' class="on"' if slug == current else ''
        n = f'<span class="num">{num}</span>' if num else '<span class="num">⌂</span>'
        rows.append(f'<li><a href="{slug}.html"{cls}>{n}<span>{html.escape(title)}</span></a></li>')
    return '<ul class="nav">' + ''.join(rows) + '</ul>'


def cards_md() -> str:
    """首頁「全部章節」：依分組產生卡片。"""
    out = []
    for g, items in GROUPS:
        if not g:
            continue
        out += [f'### {g}', '', '<div class="cards">']
        for slug, title, _, card in items:
            out.append(f'<a class="card" href="{slug}.html"><span class="n">{NUM[slug]}</span>'
                       f'<b>{html.escape(title)}</b><small>{html.escape(card)}</small></a>')
        out += ['</div>', '']
    return '\n'.join(out)


def redirect_html(old: str, vla: str, wm: str, wm_anchors) -> str:
    return f'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={vla}.html">
<title>本頁已搬家</title>
<script>var h=location.hash.slice(1),w={json.dumps(wm_anchors)};
location.replace((w.indexOf(h)>=0?'{wm}':'{vla}')+'.html'+(w.indexOf(h)>=0?'':location.hash));</script>
</head><body><p>這一頁已拆成 <a href="{vla}.html">{html.escape(dict((p[0], p[2]) for p in PAGES)[vla])}</a>
與 <a href="{wm}.html">{html.escape(dict((p[0], p[2]) for p in PAGES)[wm])}</a>。</p></body></html>
'''


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
    for i, (slug, num, title, desc, _g, _c) in enumerate(PAGES):
        src = (CONTENT / f'{slug}.md').read_text(encoding='utf-8')
        if slug == 'index':
            src = src.replace('{{CHAPTER_CARDS}}', cards_md())
        if slug == 'params':
            src = src.replace('{{PARAMS_TABLES}}', params_lib.full_tables_md())
        elif slug not in ('index', 'references', 'glossary'):
            src = src.split(params_lib.MARK)[0].rstrip() + '\n\n' + params_lib.section_md(params_lib.mentioned(src))
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
    for old, (vla, wm, anchors) in REDIRECTS.items():
        (OUT / f'{old}.html').write_text(redirect_html(old, vla, wm, anchors), encoding='utf-8')
    (OUT / '.nojekyll').write_text('')
    # 用 .js 而不是 .json：直接開本機檔案（file://）也能載入
    (OUT / 'assets' / 'search-index.js').write_text(
        'window.SITE_INDEX=' + json.dumps(index, ensure_ascii=False, separators=(',', ':')) + ';\n',
        encoding='utf-8')
    print('indexed', len(index), 'sections')


if __name__ == '__main__':
    build()
