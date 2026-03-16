#!/usr/bin/env python3
"""
ממיר.פותח.אי.py

פותח אי נעולים לפי קריטריון

סדר פתיחה (מלמעלה למטה):
1. 10 ספירות עומק
2. 22 אותיות (3 אמות, 7 כפולות, 12 פשוטות)
3. 3 יוצרים (תלי, גלגל, לב)
4. 6 קצוות
5. 12 אלכסונן
6. 32 נתיבות
7. 231 שערים
8. ... והשאר לפי צורך

מצבי סור:
- נעול: לא פעיל
- מוגבל: פעיל חלקית
- פתוח: פעיל מלא

איסורים:
- no 3rd party
"""

from pathlib import Path

BASE = Path(__file__).parent
AIN_DIR = BASE / "אין"

# סדר פתיחה
OPEN_ORDER = [
    # 10 עומק
    'עומק ראשית', 'עומק אחרית',
    'עומק טוב', 'עומק רע',
    'עומק רום', 'עומק תחת',
    'עומק מזרח', 'עומק מערב',
    'עומק צפון', 'עומק דרום',
    # 3 אמות
    'אות א', 'אות מ', 'אות ש',
    # 7 כפולות
    'אות ב', 'אות ג', 'אות ד', 'אות כ', 'אות פ', 'אות ר', 'אות ת',
    # 12 פשוטות
    'אות ה', 'אות ו', 'אות ז', 'אות ח', 'אות ט', 'אות י',
    'אות ל', 'אות נ', 'אות ס', 'אות ע', 'אות צ', 'אות ק',
    # 3 יוצרים
    'יוצר תלי', 'יוצר גלגל', 'יוצר לב',
    # 6 קצוות
    'קצה רום', 'קצה תחת', 'קצה מזרח', 'קצה מערב', 'קצה צפון', 'קצה דרום',
    # 3 יסודות
    'יסוד אש', 'יסוד מים', 'יסוד אויר',
    # 3 עולמות
    'ציר עולם', 'ציר שנה', 'ציר נפש',
]


def read_ai(path):
    """קרא אי"""
    ai = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if ':' in line:
                key, val = line.split(':', 1)
                ai[key.strip()] = val.strip()
    ai['_path'] = path
    return ai


def write_ai(ai):
    """כתוב אי"""
    path = ai['_path']
    with open(path, 'w', encoding='utf-8') as f:
        for key, val in ai.items():
            if not key.startswith('_'):
                f.write(f"{key}: {val}\n")


def open_ai(ai, level='פתוח'):
    """פתח אי"""
    ai['סור'] = level
    write_ai(ai)
    return ai


def find_ai_by_mah(mah_value):
    """מצא אי לפי מה"""
    for ai_file in AIN_DIR.glob("*.אי"):
        ai = read_ai(ai_file)
        if ai.get('מה', '').strip() == mah_value:
            return ai
    return None


def main():
    print("=" * 32)  # נתיבות
    print("ממיר פותח אי")
    print("=" * 32)  # נתיבות

    opened = 0
    not_found = 0

    print("\nפותח לפי סדר:")
    for mah in OPEN_ORDER:
        ai = find_ai_by_mah(mah)
        if ai:
            if ai.get('סור') == 'נעול':
                open_ai(ai, 'פתוח')
                print(f"  ✓ {mah}")
                opened += 1
            else:
                print(f"  - {mah} (כבר {ai.get('סור')})")
        else:
            print(f"  ✗ {mah} (לא נמצא)")
            not_found += 1

    print(f"\nסה\"כ: {opened} נפתחו, {not_found} לא נמצאו")
    print("=" * 32)  # נתיבות


if __name__ == "__main__":
    main()
