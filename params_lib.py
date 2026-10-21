"""模型參數量登錄表：data/params.json 是唯一來源。

build.py 用它產生〈參數量總表〉一頁，並在其他各頁末尾補上「本頁提到的模型參數量」。
同一份資料也用來更新專案資料夾裡的研究筆記（見 update_notes.py）。
"""
import json
import re
from pathlib import Path

DATA = Path(__file__).parent / 'data' / 'params.json'
SECTION_TITLE = '本頁提到的模型參數量'
MARK = '<!-- params:auto -->'


def load():
    d = json.loads(DATA.read_text(encoding='utf-8'))
    return [dict(e, kind='VLA') for e in d['vla']] + [dict(e, kind='世界模型') for e in d['wm']]


def _pattern(alias: str) -> re.Pattern:
    if alias.startswith('re:'):
        return re.compile(alias[3:])
    # 前後不能緊接英數字（避免 ACT 命中 CogACT、π0 命中 π0.5 / π0-FAST）
    return re.compile(r'(?<![A-Za-z0-9_.*-])' + re.escape(alias) + r'(?![A-Za-z0-9_]|\.\d|-[A-Za-z])')


def strip_for_match(text: str) -> str:
    text = text.split(MARK)[0]
    text = re.sub(r'<svg.*?</svg>', ' ', text, flags=re.S)
    text = re.sub(r'\]\([^)]*\)', ']', text)  # 連結網址不算提到
    return text


def mentioned(text: str, entries=None):
    entries = entries or load()
    body = strip_for_match(text)
    return [e for e in entries if any(_pattern(a).search(body) for a in e['alias'])]


def _row(e, with_detail=False):
    cells = [e['name'], e['params']]
    if with_detail:
        cells = [e['name'], e['org'], e['params'], e['detail']]
    cells.append(f"[來源]({e['src']})")
    return '| ' + ' | '.join(c.replace('|', '／') for c in cells) + ' |'


def section_md(entries, heading='##') -> str:
    if not entries:
        return ''
    lines = [MARK, '', f'{heading} {SECTION_TITLE}', '',
             '只列官方論文、官方頁或官方模型卡寫明的數字；查不到的標「未公開」，不推測。完整清單見 [參數量總表](params.html)。', '']
    for kind in ('VLA', '世界模型'):
        group = [e for e in entries if e['kind'] == kind]
        if not group:
            continue
        lines += [f'**{kind}**', '', '| 模型 | 參數量 | 來源 |', '|---|---|---|']
        lines += [_row(e) for e in group]
        lines.append('')
    return '\n'.join(lines)


def full_tables_md() -> str:
    entries = load()
    out = []
    for kind, title in (('VLA', '## VLA 與相關策略模型'), ('世界模型', '## 世界模型與影片生成模型')):
        group = [e for e in entries if e['kind'] == kind]
        out += [title, '', f'共 {len(group)} 個。', '',
                '| 模型 | 機構與年份 | 參數量 | 結構重點 | 來源 |', '|---|---|---|---|---|']
        out += [_row(e, True) for e in group]
        out.append('')
    return '\n'.join(out)
