#!/usr/bin/env python3
"""
ממיר.תיקון.כפילות.py

תיקון כפילות אותיות:
- "אות אלף" וכו' (9975-9996) → "אבם א" וכו'

אבם = צופה א עד ת ממשק-ים
- ב-שלשים פל-י-או"ת
- ב עד ש ועשר ספירות עומק לכל אות
- shared bus חכמה
- direction: הבן בחכמה חכם בבינה

איסורים:
- no 3rd party
"""

from pathlib import Path

BASE = Path(__file__).parent
AIN_DIR = BASE / "אין"

# מיפוי שמות מלאים לאותיות
FULL_TO_LETTER = {
    'אלף': 'א', 'בית': 'ב', 'גימל': 'ג', 'דלת': 'ד',
    'הא': 'ה', 'וו': 'ו', 'זין': 'ז', 'חית': 'ח',
    'טית': 'ט', 'יוד': 'י', 'כף': 'כ', 'למד': 'ל',
    'מם': 'מ', 'נון': 'נ', 'סמך': 'ס', 'עין': 'ע',
    'פא': 'פ', 'צדי': 'צ', 'קוף': 'ק', 'ריש': 'ר',
    'שין': 'ש', 'תו': 'ת'
}


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


def main():
    print("=" * 50)
    print("תיקון כפילות אותיות")
    print("אות X → אבם X (צופה ממשק)")
    print("=" * 50)

    fixed = 0

    for ai_file in AIN_DIR.glob("*.אי"):
        ai = read_ai(ai_file)
        mah = ai.get('מה', '')
        makor = ai.get('מקור', '')

        # מצא כפילויות מ"ספר יצירה - סיום"
        if mah.startswith('אות ') and makor == 'ספר יצירה - סיום':
            # חלץ שם מלא
            full_name = mah.replace('אות ', '')

            if full_name in FULL_TO_LETTER:
                letter = FULL_TO_LETTER[full_name]

                # שנה ל-אבם
                ai['מה'] = f'אבם {letter}'
                ai['מקור'] = 'אברהם - אבם צופה'
                ai['שם_מלא'] = full_name
                ai['תפקיד'] = 'ממשק צופה'
                ai['bus'] = 'חכמה'
                ai['direction'] = 'הבן בחכמה חכם בבינה'

                write_ai(ai)
                print(f"  {mah} → אבם {letter}")
                fixed += 1

    print(f"\nסה\"כ: {fixed} תוקנו")
    print("=" * 50)


if __name__ == "__main__":
    main()
