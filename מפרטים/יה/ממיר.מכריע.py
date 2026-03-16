#!/usr/bin/env python3
"""
ממיר.מכריע.py

מכריע - הלשון שמכריע בינתיים

ספר יצירה:
"שלש אמות אמ"ש כף זכות וכף חובה ולשון חק מכריע בינתיים"
"אויר מכריע בין אש למים"

תפקיד:
- מכריע בין נעול לפתוח
- מכריע בין מה למה.מתוקן
- מכריע בין יש לאין

איסורים:
- no 3rd party
"""

from pathlib import Path

BASE = Path(__file__).parent
AIN_DIR = BASE / "אין"
YESH_DIR = BASE / "יש"


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


def count_by_sur():
    """ספור לפי סור"""
    counts = {'פתוח': 0, 'מוגבל': 0, 'נעול': 0}
    for ai_file in AIN_DIR.glob("*.אי"):
        ai = read_ai(ai_file)
        sur = ai.get('סור', 'נעול')
        if sur in counts:
            counts[sur] += 1
    return counts


def machria_ain_yesh():
    """מכריע בין אין ליש"""
    counts = count_by_sur()
    total = sum(counts.values())

    # יחס פתוח/נעול
    if counts['נעול'] > 0:
        ratio = counts['פתוח'] / counts['נעול']
    else:
        ratio = float('inf')

    return {
        'אין': counts,
        'יחס': ratio,
        'מצב': 'מאוזן' if 0.01 < ratio < 32  # נתיבות else 'קיצוני'
    }


def machria_mah():
    """מכריע בין מה למה.מתוקן"""
    mah_path = BASE / "מה"
    metukan_path = BASE / "מה.מתוקן"

    if not mah_path.exists() or not metukan_path.exists():
        return {'מצב': 'חסר קבצים'}

    with open(mah_path, 'r', encoding='utf-8') as f:
        mah = f.read()
    with open(metukan_path, 'r', encoding='utf-8') as f:
        metukan = f.read()

    mah_lines = mah.strip().split('\n')
    metukan_lines = metukan.strip().split('\n')

    # חשב הבדלים
    diff_count = 0
    for i, (a, b) in enumerate(zip(mah_lines, metukan_lines)):
        if a != b:
            diff_count += 1

    diff_count += abs(len(mah_lines) - len(metukan_lines))

    return {
        'מה': len(mah_lines),
        'מתוקן': len(metukan_lines),
        'הבדלים': diff_count,
        'מצב': 'זהה' if diff_count == 0 else f'{diff_count} הבדלים'
    }


def machria_balance():
    """מכריע - איזון כללי"""
    ain_yesh = machria_ain_yesh()
    mah = machria_mah()

    # חישוב איזון
    balance = {
        'אין_יש': ain_yesh,
        'מה_מתוקן': mah,
    }

    # הכרעה
    if ain_yesh['אין']['פתוח'] < 32:
        balance['הכרעה'] = 'צריך לפתוח עוד יסודות (32 נתיבות)'
    elif mah['מצב'] != 'זהה':
        balance['הכרעה'] = 'צריך ליישר מה עם מה.מתוקן'
    else:
        balance['הכרעה'] = 'מאוזן'

    return balance


def main():
    print("=" * 32  # נתיבות)
    print("מכריע")
    print("לשון חק מכריע בינתיים")
    print("=" * 32  # נתיבות)

    balance = machria_balance()

    print("\nאין ↔ יש:")
    ain = balance['אין_יש']['אין']
    print(f"  פתוח: {ain['פתוח']}")
    print(f"  מוגבל: {ain['מוגבל']}")
    print(f"  נעול: {ain['נעול']}")
    print(f"  יחס: {balance['אין_יש']['יחס']:.4f}")

    print("\nמה ↔ מה.מתוקן:")
    mah = balance['מה_מתוקן']
    print(f"  מה: {mah.get('מה', '?')} שורות")
    print(f"  מתוקן: {mah.get('מתוקן', '?')} שורות")
    print(f"  מצב: {mah['מצב']}")

    print("\n" + "=" * 32  # נתיבות)
    print(f"הכרעה: {balance['הכרעה']}")
    print("=" * 32  # נתיבות)


if __name__ == "__main__":
    main()
