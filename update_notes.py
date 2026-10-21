"""把參數量登錄表同步到專案資料夾的研究筆記（不在網站 repo 內）。

用法：python3 update_notes.py /mnt/project-files/research
"""
import sys
from pathlib import Path

import params_lib

NOTE = 'model-parameters.md'


def main(folder: str):
    d = Path(folder)
    full = ('# VLA 與世界模型參數量總表\n\n'
            '> 只列官方論文、官方頁或官方模型卡寫明的數字；查不到的標「未公開」，不推測。'
            '資料與網站〈參數量總表〉同一份（repo 的 data/params.json）。\n\n'
            + params_lib.full_tables_md())
    (d / NOTE).write_text(full, encoding='utf-8')
    for f in sorted(d.glob('*.md')):
        if f.name == NOTE:
            continue
        text = f.read_text(encoding='utf-8')
        sec = params_lib.section_md(params_lib.mentioned(text)).replace('(params.html)', f'({NOTE})')
        base = text.split(params_lib.MARK)[0].rstrip()
        f.write_text(base + ('\n\n---\n\n' + sec if sec else '') + '\n', encoding='utf-8')
        print(f.name, 'updated')


if __name__ == '__main__':
    main(sys.argv[1])
