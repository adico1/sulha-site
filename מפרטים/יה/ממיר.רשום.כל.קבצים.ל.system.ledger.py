#!/usr/bin/env python3
"""
ממיר.רשום.כל.קבצים.ל.system.ledger.py

נוצר אוטומטית על ידי אברם
לומד פעולה חדשה: רשום_כל_קבצים_ל_system_ledger

מקור: ספר יצירה שורה 23 - צופה וממיר
"""

from pathlib import Path

BASE = Path(__file__).parent

def main():
    print("=" * 32)  # נתיבות - מספר יצירה
    print("רשום_כל_קבצים_ל_system_ledger")
    print("=" * 32)  # נתיבות - מספר יצירה

    import os
    from datetime import datetime
    
    ROOT = BASE.parent.parent.parent
    LEDGER = ROOT / 'system.ledger'
    
    def escape(s):
        return s.replace('\\', '\\\\').replace('|', '\\|').replace('\n', '\\n')
    
    # get existing
    existing = set()
    if LEDGER.exists():
        with open(LEDGER, 'r', encoding='utf-8') as f:
            for line in f:
                if '|l:' in line:
                    for p in line.split('|'):
                        if p.startswith('l:'):
                            existing.add(p[2:])
    
    # get next bid
    next_bid = 1
    if LEDGER.exists():
        with open(LEDGER, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('bid:'):
                    bid = int(line.split('|')[0].split(':')[1])
                    next_bid = max(next_bid, bid + 1)
    
    registered = 0
    with open(LEDGER, 'a', encoding='utf-8') as ledger:
        for root, dirs, files in os.walk(ROOT):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for fname in files:
                if fname.startswith('.'):
                    continue
                fpath = Path(root) / fname
                rel = str(fpath.relative_to(ROOT))
                if rel in existing:
                    continue
                stat = fpath.stat()
                content = ''
                if fpath.suffix in ['.py', '.txt', '.md']:
                    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                ledger.write(f'bid:{next_bid}|l:{rel}|n:{fpath.stem}|e:{fpath.suffix}|p:{fpath.parent.name}\n')
                ledger.write(f'bid:{next_bid}|size:{stat.st_size}|created:{datetime.fromtimestamp(stat.st_ctime).isoformat()}|modified:{datetime.fromtimestamp(stat.st_mtime).isoformat()}\n')
                ledger.write(f'bid:{next_bid}|crystallized:false|content:{escape(content)}\n')
                next_bid += 1
                registered += 1
    
    print(f'נרשמו {registered} קבצים חדשים')
    print(f'סה"כ: {next_bid - 1} רשומות')

if __name__ == "__main__":
    main()
